class ChatSession:
    def __init__(self):
        self.history = []

    def add_user_message(self, msg):
        self.history.append({"role": "user", "content": msg})

    def add_assistant_message(self, msg):
        self.history.append({"role": "assistant", "content": msg})

    def get_recent_history(self, max_turns=6):
        return self.history[-max_turns:]
