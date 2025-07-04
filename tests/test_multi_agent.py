import os
import sys

project_root = os.path.dirname(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.multi_agent import MultiAgentCoordinator
from core.agents.base import Agent


class AgentA(Agent):
    def act(self, message: str, context: dict):
        context.setdefault("order", []).append("A")
        return message + "a", context


class AgentB(Agent):
    def act(self, message: str, context: dict):
        context.setdefault("order", []).append("B")
        return message + "b", context


class DummyTTSAgent(Agent):
    def __init__(self):
        from core.agents.tts_agent import TTSAgent

        self.inner = TTSAgent()

    def act(self, message: str, context: dict):
        return self.inner.act(message, context)


def test_multi_agent_coordinator_shared_context():
    coord = MultiAgentCoordinator([AgentA(), AgentB()])
    result = coord.run("x")
    assert result == "xab"
    assert coord.context["order"] == ["A", "B"]


def test_tts_agent_in_pipeline(monkeypatch):
    # Stub the text_to_speech function so tests don't hit network
    import utilities.text_to_speech as tts
    import core.agents.tts_agent as ttsa

    monkeypatch.setattr(tts, "text_to_speech_base64", lambda text, lang="en": "audio")
    monkeypatch.setattr(ttsa, "text_to_speech_base64", lambda text, lang="en": "audio")

    coord = MultiAgentCoordinator([DummyTTSAgent()])
    result = coord.run("hello")
    assert result == "hello"
    assert coord.context["audio"] == "audio"
