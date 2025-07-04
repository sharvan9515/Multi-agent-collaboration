"""Interfaces for workflow hooks allowing custom pre/post processing."""

from __future__ import annotations

from typing import Protocol, Tuple, Dict

from agents.base import Agent


class WorkflowHook(Protocol):
    """Hook interface for Workflow events."""

    def before_agent(self, agent: Agent, message: str, context: Dict) -> Tuple[str, Dict]:  # pragma: no cover - interface
        ...

    def after_agent(self, agent: Agent, message: str, context: Dict) -> Tuple[str, Dict]:  # pragma: no cover - interface
        ...

