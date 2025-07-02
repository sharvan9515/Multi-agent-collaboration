import os
import sys

project_root = os.path.dirname(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.multi_agent import MultiAgentCoordinator
from agents.base import Agent


class AgentA(Agent):
    def act(self, message: str, context: dict):
        context.setdefault("order", []).append("A")
        return message + "a", context


class AgentB(Agent):
    def act(self, message: str, context: dict):
        context.setdefault("order", []).append("B")
        return message + "b", context


def test_multi_agent_coordinator_shared_context():
    coord = MultiAgentCoordinator([AgentA(), AgentB()])
    result = coord.run("x")
    assert result == "xab"
    assert coord.context["order"] == ["A", "B"]
