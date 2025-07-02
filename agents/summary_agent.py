from .base import Agent


class SummaryAgent(Agent):
    """Agent that returns a short summary of the message."""

    def act(self, message: str, context: dict) -> tuple[str, dict]:
        summary = message[:100]
        context["summary"] = summary
        return summary, context
