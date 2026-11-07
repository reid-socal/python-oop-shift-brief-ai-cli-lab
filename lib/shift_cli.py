Shift cli · PY
from ai_client import OllamaChatClient
from brief_builder import HandoffBriefBuilder
 
 
class ShiftBriefCLI:
    """Command-line workflow for generating and revising shift handoff briefs."""
 
    def __init__(self, ai_client, brief_builder=None):
        """Initialize the CLI with an injected AI client and optional builder."""
        self.ai_client = ai_client
        self.brief_builder = brief_builder or HandoffBriefBuilder()
        self.running = True
 
    def display_welcome(self):
        """Print a welcome message and command guidance."""
        print("Shift Handoff Brief CLI")
        print("Create and revise AI-assisted shift handoff briefs.")
        print()
        print(self.command_help())
        print()
 
    def command_help(self):
        """Return command guidance as a string."""
        return (
            "Commands:\n"
            "- brief <shift notes>     Create a new handoff brief.\n"
            "- revise <feedback>       Revise the previous brief using feedback.\n"
            "- history                 Show the current conversation message count.\n"
            "- reset                   Clear conversation history.\n"
            "- help                    Show this command list.\n"
            "- exit or quit            Stop the program."
        )
 
    def handle_command(self, raw_input):
        """Route a user command and return the message to display."""
        if not isinstance(raw_input, str) or not raw_input.strip():
            return "Input Error: Please enter a command. Type 'help' to see the commands."
 
        parts = raw_input.strip().split(None, 1)
        command = parts[0].lower()
        payload = parts[1].strip() if len(parts) > 1 else ""
 
        try:
            if command == "brief":
                if not payload:
                    return "Input Error: Please provide shift notes after 'brief'."
                return self.brief_builder.create_brief(self.ai_client, payload)
 
            if command == "revise":
                if not payload:
                    return "Input Error: Please provide revision feedback after 'revise'."
                return self.brief_builder.revise_brief(self.ai_client, payload)
 
            if command == "history":
                return f"Conversation messages: {self.ai_client.message_count()}"
 
            if command == "reset":
                self.ai_client.reset()
                return "Conversation history reset."
 
            if command == "help":
                return self.command_help()
 
            if command in ("exit", "quit"):
                self.running = False
                return "Goodbye!"
 
            return (
                f"Input Error: Unknown command '{parts[0]}'. "
                "Type 'help' to see the available commands."
            )
        except ValueError as error:
            return f"Input Error: {error}"
        except RuntimeError as error:
            return f"Service Error: {error}"
 
    def run(self):
        """Run the CLI input loop."""
        self.display_welcome()
 
        while self.running:
            try:
                user_input = input("> ")
            except EOFError:
                break
 
            print(self.handle_command(user_input))
 
 
def main():
    client = OllamaChatClient(model_name="llama3.2")
    app = ShiftBriefCLI(client)
    app.run()
 
 
if __name__ == "__main__":
    main()
 