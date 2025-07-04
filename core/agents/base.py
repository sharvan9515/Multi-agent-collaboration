from typing import Dict, Tuple


class Agent:
    """Abstract agent interface for all agents."""

    def act(self, message: str, context: Dict) -> Tuple[str, Dict]:
        """Process a message and update the shared context."""
        raise NotImplementedError("Agents must implement the act method")
