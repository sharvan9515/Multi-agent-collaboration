import os
import sys
import types
import pkgutil

project_root = os.path.dirname(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from agents.base import Agent  # noqa: E402


class AgentA(Agent):
    def act(self, message: str, context: dict):
        context.setdefault("order", []).append("A")
        return message + "a", context


class AgentB(Agent):
    def act(self, message: str, context: dict):
        context.setdefault("order", []).append("B")
        return message + "b", context


# Stub generate_answer to control routing decisions
responses = iter(["AgentA", "AgentB", "FINISH"])


def fake_generate_answer(messages):
    return next(responses)


import importlib
import language_model.language_model as lm_mod  # type: ignore
lm_mod.generate_answer = fake_generate_answer

import core.supervisor as sup_mod  # noqa: E402
importlib.reload(sup_mod)
LLMSupervisor = sup_mod.LLMSupervisor
AdvancedSupervisor = sup_mod.AdvancedSupervisor
discover_agents = sup_mod.discover_agents


def test_llm_supervisor_runs_agents_in_order():
    sup = LLMSupervisor({"AgentA": AgentA(), "AgentB": AgentB()})
    result = sup.run("x")
    assert result == "xab"
    assert sup.context["order"] == ["A", "B"]


def test_discover_agents_loads_custom_package(monkeypatch):
    fakepkg = types.ModuleType("fakepkg")
    fakepkg.__path__ = ["fake"]

    mod1 = types.ModuleType("fakepkg.mod1")

    class AgentX(Agent):
        def act(self, message: str, context: dict):
            return "x", context

    mod1.AgentX = AgentX

    mod2 = types.ModuleType("fakepkg.mod2")

    class AgentY(Agent):
        def act(self, message: str, context: dict):
            return "y", context

    mod2.AgentY = AgentY

    monkeypatch.setitem(sys.modules, "fakepkg", fakepkg)
    monkeypatch.setitem(sys.modules, "fakepkg.mod1", mod1)
    monkeypatch.setitem(sys.modules, "fakepkg.mod2", mod2)

    monkeypatch.setattr(pkgutil, "iter_modules", lambda path: [
        types.SimpleNamespace(name="mod1"),
        types.SimpleNamespace(name="mod2"),
    ])

    agents = discover_agents("fakepkg")
    assert set(agents) == {"AgentX", "AgentY"}

    sup = LLMSupervisor(agents)
    assert sorted(sup.available_agents()) == ["AgentX", "AgentY"]


class SummarizerStub(Agent):
    def act(self, message: str, context: dict):
        return "summary", context


def test_advanced_supervisor_summarizes_history(monkeypatch):
    responses = iter(["AgentA", "FINISH"])
    lm_mod.generate_answer = lambda _: next(responses)
    sup_mod.generate_answer = lm_mod.generate_answer

    sup = AdvancedSupervisor(
        {"AgentA": AgentA()},
        max_history=1,
        summarizer=SummarizerStub(),
    )

    sup.run("x")
    assert sup.context["messages"] == [{"role": "system", "content": "summary"}]


def test_advanced_supervisor_respects_max_turns(monkeypatch):
    responses = iter(["AgentA", "AgentB", "AgentA"])
    lm_mod.generate_answer = lambda _: next(responses)
    sup_mod.generate_answer = lm_mod.generate_answer

    sup = AdvancedSupervisor(
        {"AgentA": AgentA(), "AgentB": AgentB()},
        max_turns=2,
        summarizer=SummarizerStub(),
    )

    sup.run("x")
    assert sup.context["order"] == ["A", "B"]
