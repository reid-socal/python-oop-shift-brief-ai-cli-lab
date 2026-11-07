import ollama


class OllamaChatClient:
    """Generic reusable client for interacting with a local chat model service."""

    def __init__(self, model_name="llama3.2"):
        """Initialize the client with a model name and its own empty history."""
        self.model_name = model_name
        self.history = []

    def send(self, prompt):
        """
        Send a prompt to the AI service and return the assistant response text.

        Raises ValueError for blank prompts and RuntimeError for service-level
        failures. On failure, the user message that was just added is removed
        so earlier valid history is preserved.
        """
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        user_message = {"role": "user", "content": prompt.strip()}
        self.history.append(user_message)

        try:
            response = ollama.chat(model=self.model_name, messages=self.history)
            assistant_text = self._extract_content(response)
        except Exception as error:
            self._remove_message(user_message)
            raise RuntimeError(f"AI service request failed: {error}") from error

        self.history.append({"role": "assistant", "content": assistant_text})
        return assistant_text

    def reset(self):
        """Clear the conversation history."""
        self.history = []

    def message_count(self):
        """Return the number of stored messages (user and assistant)."""
        return len(self.history)

    def get_transcript(self):
        """Return a safe copy of the conversation history."""
        return [message.copy() for message in self.history]

    def _remove_message(self, message):
        """Remove a specific message object from history if it is present."""
        for index in range(len(self.history) - 1, -1, -1):
            if self.history[index] is message:
                del self.history[index]
                return

    @staticmethod
    def _get_field(container, name):
        """Read a field from a dict-style or object-style value."""
        if isinstance(container, dict):
            return container.get(name)
        return getattr(container, name, None)

    def _extract_content(self, response):
        """Return usable assistant text from a dict or object response."""
        message = self._get_field(response, "message")

        if message is None:
            raise ValueError("Response did not include a message.")

        content = self._get_field(message, "content")

        if not isinstance(content, str) or not content.strip():
            raise ValueError("Response did not include usable assistant content.")

        return content