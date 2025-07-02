from typing import List, Tuple, Dict

from utils.logger import log
from agents.base import Agent


class MultiAgentCoordinator:
    """Coordinate multiple agents sharing a mutable context."""

    def __init__(self, agents: List[Agent]):
        self.agents = agents
        self.context: Dict = {"messages": []}

    def run(self, message: str) -> str:
        """Send the message through each agent with shared context."""
        log(f"Starting multi-agent run with input: {message}")
        msg = message
        for agent in self.agents:
            msg, self.context = agent.act(msg, self.context)
            log(f"{agent.__class__.__name__} produced: {msg}")
        return msg
