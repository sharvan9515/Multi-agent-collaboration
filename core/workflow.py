from typing import List

from utils.logger import log
from agents.base import Agent


class Workflow:
    """Simple sequential workflow that runs a list of agents."""

    def __init__(self, agents: List[Agent]):
        self.agents = agents

    def run(self, message: str) -> str:
        """Send the message through each agent in sequence."""
        log(f"Starting workflow with input: {message}")
        for agent in self.agents:
            message = agent.act(message)
            log(f"{agent.__class__.__name__} produced: {message}")
        return message
