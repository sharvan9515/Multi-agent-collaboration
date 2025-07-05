from typing import List


from utils.event_bus import event_bus
from utils.metrics import AGENT_RUNS, WORKFLOW_SECONDS
from core.hooks import WorkflowHook

from utils.logger import log
from agents.base import Agent


class Workflow:
    """Simple sequential workflow that runs a list of agents."""

    def __init__(self, agents: List[Agent], hooks: List[WorkflowHook] | None = None):
        """Create a workflow, ensuring security checks precede any RAG agent."""
        new_agents: List[Agent] = []
        security_inserted = False
        for agent in agents:
            if agent.__class__.__name__ == "SecurityAgent":
                security_inserted = True
                new_agents.append(agent)
                continue

            if agent.__class__.__name__ == "RAGAgent" and not security_inserted:
                from agents.security_agent import SecurityAgent
                new_agents.append(SecurityAgent())
                security_inserted = True
            new_agents.append(agent)

        self.agents = new_agents
        self.hooks = hooks or []

    def run(self, message: str) -> str:
        """Send the message through each agent in sequence with shared context."""
        cid = log(f"Starting workflow with input: {message}")
        context = {}
        msg = message

        if WORKFLOW_SECONDS:
            timer = WORKFLOW_SECONDS.time()
        else:
            timer = None

        event_bus.emit("workflow_start", message=message)

        for agent in self.agents:
            event_bus.emit("agent_start", agent=agent.__class__.__name__)

            for hook in self.hooks:
                msg, context = hook.before_agent(agent, msg, context)

            msg, context = agent.act(msg, context)

            for hook in self.hooks:
                msg, context = hook.after_agent(agent, msg, context)

            if AGENT_RUNS:
                AGENT_RUNS.labels(agent=agent.__class__.__name__).inc()
            event_bus.emit("agent_end", agent=agent.__class__.__name__, message=msg)
            log(f"{agent.__class__.__name__} produced: {msg}", cid)

        event_bus.emit("workflow_end", message=msg, context=context)

        if timer:
            timer.observe_duration()

        return msg
