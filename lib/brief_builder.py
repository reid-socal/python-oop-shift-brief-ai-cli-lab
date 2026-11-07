class HandoffBriefBuilder:
    """Builds prompts and verifies output for shift handoff briefs."""
 
    REQUIRED_SECTIONS = (
        "Shift Summary:",
        "Open Issues:",
        "Action Items:",
        "Follow-Up Questions:",
        "Risk Notes:",
    )
 
    def _section_list(self):
        """Return the required section labels, one per line."""
        return "\n".join(self.REQUIRED_SECTIONS)
 
    def build_brief_prompt(self, notes):
        """Build a prompt for creating a new shift handoff brief."""
        if not isinstance(notes, str) or not notes.strip():
            raise ValueError("Shift notes cannot be empty.")
 
        return (
            "You are helping a retail store team write a shift handoff brief "
            "from messy shift notes.\n\n"
            "Create a shift handoff brief that uses exactly these section "
            "labels, each on its own line:\n"
            f"{self._section_list()}\n\n"
            "Rules:\n"
            "- Only use details that appear in the shift notes.\n"
            "- Do not invent or assume details that are not in the notes.\n"
            "- If a detail is not provided, write Unknown.\n"
            "- Keep the writing clear and practical for the next shift.\n\n"
            "Shift notes:\n"
            f"{notes.strip()}"
        )
 
    def build_revision_prompt(self, feedback):
        """Build a prompt for revising the previous handoff brief."""
        if not isinstance(feedback, str) or not feedback.strip():
            raise ValueError("Revision feedback cannot be empty.")
 
        return (
            "Revise the previous shift handoff brief from earlier in this "
            "conversation, using the manager's feedback below.\n\n"
            "Return the full revised brief using exactly these section "
            "labels, each on its own line:\n"
            f"{self._section_list()}\n\n"
            "Rules:\n"
            "- Only use details from the original shift notes and the "
            "previous brief.\n"
            "- Do not invent or assume details that are not provided.\n"
            "- If a detail is not provided, write Unknown.\n\n"
            "Manager feedback:\n"
            f"{feedback.strip()}"
        )
 
    def is_usable_brief(self, response_text):
        """Return True only if the response contains every required section."""
        if not isinstance(response_text, str) or not response_text.strip():
            return False
 
        return all(section in response_text for section in self.REQUIRED_SECTIONS)
 
    def format_brief(self, response_text, heading="Shift Handoff Brief"):
        """Format a handoff brief for display with a clear heading."""
        return f"\n{heading}\n{response_text}"
 
    def _check_response(self, response_text):
        """Raise RuntimeError when the response lacks the required structure."""
        if not self.is_usable_brief(response_text):
            raise RuntimeError(
                "AI response did not include required sections: "
                + ", ".join(self.REQUIRED_SECTIONS)
            )
 
    def create_brief(self, ai_client, notes):
        """Create a new handoff brief through the AI client."""
        prompt = self.build_brief_prompt(notes)
        response_text = ai_client.send(prompt)
        self._check_response(response_text)
        return self.format_brief(response_text)
 
    def revise_brief(self, ai_client, feedback):
        """Revise the previous handoff brief through the AI client."""
        prompt = self.build_revision_prompt(feedback)
        response_text = ai_client.send(prompt)
        self._check_response(response_text)
        return self.format_brief(response_text, heading="Revised Shift Handoff Brief")
 