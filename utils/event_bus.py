class EventBus:
    """Simple synchronous event bus for emitting and subscribing to events."""

    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_name: str, handler):
        """Register a handler for a specific event."""
        handlers = self._subscribers.setdefault(event_name, [])
        handlers.append(handler)

    def emit(self, event_name: str, **data):
        """Emit an event to all subscribed handlers."""
        for handler in self._subscribers.get(event_name, []):
            try:
                handler(event_name, **data)
            except Exception as exc:  # pragma: no cover - handler errors shouldn't crash
                print(f"Event handler error: {exc}")


event_bus = EventBus()
