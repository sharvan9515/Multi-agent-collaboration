import os
import sys

project_root = os.path.dirname(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from agents.base import Agent  # noqa: E402
from core.workflow import Workflow  # noqa: E402


class UpperHook:
    def before_agent(self, agent, message, context):
        return message.upper(), context

    def after_agent(self, agent, message, context):
        context['after'] = True
        return message, context


class EchoAgent(Agent):
    def act(self, message, context):
        return message + "!", context


def test_workflow_hook_modifies_message():
    wf = Workflow([EchoAgent()], hooks=[UpperHook()])
    result = wf.run("hello")
    assert result == "HELLO!"

