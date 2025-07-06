from __future__ import annotations

from typing import Dict, List
import importlib
import pkgutil

from agents.base import Agent
from utils.logger import log
from utils.event_bus import event_bus
from utils.metrics import AGENT_RUNS, WORKFLOW_SECONDS
from language_model.language_model import generate_answer


def discover_agents(package: str = "agents") -> Dict[str, Agent]:
    """Import all Agent subclasses from the given package."""
    pkg = importlib.import_module(package)
    discovered: Dict[str, Agent] = {}
    for mod_info in pkgutil.iter_modules(pkg.__path__):
        module = importlib.import_module(f"{package}.{mod_info.name}")
        for name, obj in vars(module).items():
            if (
                isinstance(obj, type)
                and issubclass(obj, Agent)
                and obj is not Agent
            ):
                try:
                    discovered[name] = obj()
                except Exception:
                    log(f"Failed to instantiate agent {name}")
    return discovered


class LLMSupervisor:
    """Coordinate agents using an LLM to dynamically choose the next step."""

    def __init__(self, agents: Dict[str, Agent] | None = None, system_prompt: str | None = None):
        agents = agents or discover_agents()
        if not agents:
            raise ValueError("At least one agent must be provided")
        self.agents = agents
        self.context: Dict = {"messages": []}
        self.system_prompt = system_prompt or self._default_prompt()

    @classmethod
    def from_package(cls, package: str = "agents", **kwargs) -> "LLMSupervisor":
        """Create a supervisor loading all agents from ``package``."""
        return cls(discover_agents(package), **kwargs)

    def register_agent(self, name: str, agent: Agent) -> None:
        """Add or replace an agent used by the supervisor."""
        self.agents[name] = agent

    def unregister_agent(self, name: str) -> None:
        """Remove an agent by name if present."""
        self.agents.pop(name, None)

    def available_agents(self) -> List[str]:
        """Return the list of currently registered agent names."""
        return list(self.agents.keys())

    def _default_prompt(self) -> str:
        return (
            "You are a supervisor that manages the following agents: "
            + ", ".join(self.agents.keys())
            + ". After each response decide which agent should act next or reply FINISH."
        )

    def _route(self) -> str:
        """Ask the language model which agent should run next."""
        options = list(self.agents.keys()) + ["FINISH"]
        messages: List[dict] = (
            [{"role": "system", "content": self.system_prompt}]
            + self.context["messages"]
            + [
                {
                    "role": "system",
                    "content": f"Who should act next? Options: {options}",
                }
            ]
        )
        response = generate_answer(messages)
        choice = response.strip()
        if choice not in options:
            choice = "FINISH"
        return choice

    def run(self, message: str) -> str:
        cid = log(f"Starting LLMSupervisor run with input: {message}")
        self.context["messages"].append({"role": "user", "content": message})

        if WORKFLOW_SECONDS:
            timer = WORKFLOW_SECONDS.time()
        else:
            timer = None

        event_bus.emit("workflow_start", message=message)

        msg = message
        next_agent = self._route()
        while next_agent != "FINISH":
            agent = self.agents.get(next_agent)
            if agent is None:
                break
            event_bus.emit("agent_start", agent=next_agent)
            msg, self.context = agent.act(msg, self.context)
            self.context["messages"].append({"role": "assistant", "content": msg})
            if AGENT_RUNS:
                AGENT_RUNS.labels(agent=next_agent).inc()
            event_bus.emit("agent_end", agent=next_agent, message=msg)
            log(f"{next_agent} produced: {msg}", cid)
            next_agent = self._route()

        event_bus.emit(
            "workflow_end", message=msg, context=self.context
        )
        if timer:
            timer.observe_duration()
        return msg
