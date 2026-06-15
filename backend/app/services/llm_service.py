from __future__ import annotations

from app.core.config import settings


class LLMService:
    def __init__(self) -> None:
        self.api_key = settings.anthropic_api_key

    def generate_text(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is required to generate plans and reports")

        from langchain_anthropic import ChatAnthropic

        model = ChatAnthropic(
            api_key=self.api_key,
            model="claude-sonnet-4-6",
            temperature=0.2,
        )
        response = model.invoke(prompt)
        return response.content


llm_service = LLMService()
