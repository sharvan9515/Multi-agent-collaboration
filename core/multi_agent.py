from typing import List, Dict

from utils.logger import log
from utils.event_bus import event_bus
from utils.metrics import AGENT_RUNS, WORKFLOW_SECONDS
from agents.base import Agent


class MultiAgentCoordinator:
    """Coordinate multiple agents sharing a mutable context."""

    def __init__(self, agents: List[Agent]):
        self.agents = agents
        self.context: Dict = {"messages": []}

    def run(self, message: str) -> str:
        """Send the message through each agent with shared context."""
        cid = log(f"Starting multi-agent run with input: {message}")
        msg = message

        if WORKFLOW_SECONDS:
            timer = WORKFLOW_SECONDS.time()
        else:
            timer = None

        event_bus.emit("workflow_start", message=message)

        for agent in self.agents:
            event_bus.emit("agent_start", agent=agent.__class__.__name__)
            msg, self.context = agent.act(msg, self.context)
            if AGENT_RUNS:
                AGENT_RUNS.labels(agent=agent.__class__.__name__).inc()
            event_bus.emit("agent_end", agent=agent.__class__.__name__, message=msg)
            log(f"{agent.__class__.__name__} produced: {msg}", cid)

        event_bus.emit("workflow_end", message=msg, context=self.context)
        if timer:
            timer.observe_duration()
        return msg
