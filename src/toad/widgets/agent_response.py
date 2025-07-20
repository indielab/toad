import llm

from textual import work
from textual.widgets import Markdown
from toad import messages

SYSTEM = """\
You are an intern at a tech company.
It is your job to generate code when asked.
Add inline documentation to your code, and always use type hinting where appropriate.
Include all imports required for the code to run.
Limit your responses to the requested code with little additional detail.
"""


class AgentResponse(Markdown):
    def __init__(self, markdown: str | None = None) -> None:
        self.model = llm.get_model("gpt-4o")
        super().__init__(markdown)

    @work(thread=True)
    def send_prompt(self, prompt: str) -> None:
        """Get the response in a thread."""
        self.post_message(messages.WorkStarted())
        llm_response = self.model.prompt(prompt, system=SYSTEM)
        for chunk in llm_response:
            self.app.call_from_thread(self.append, chunk)
        self.post_message(messages.WorkFinished())
