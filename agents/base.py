class Agent:
    """Abstract agent interface."""
    def act(self, message: str) -> str:
        raise NotImplementedError("Agents must implement the act method")
