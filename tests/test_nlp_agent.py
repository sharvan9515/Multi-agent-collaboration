import os
import sys

project_root = os.path.dirname(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from agents.nlp_agent import NLPAgent  # noqa: E402


def test_nlp_agent_keywords():
    agent = NLPAgent(["this is a test corpus"])
    msg = "this test"
    out, ctx = agent.act(msg, {})
    assert "Keywords" in out
    assert ctx["keywords"]
