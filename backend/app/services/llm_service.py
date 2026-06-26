from __future__ import annotations

from app.core.config import settings


class LLMService:
    def __init__(self) -> None:
        self.api_key = settings.groq_api_key

    def generate_text(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("GROQ_API_KEY is required to generate plans and reports")

        from langchain_groq import ChatGroq

        model = ChatGroq(
            api_key=self.api_key,
            model="mixtral-8x7b-32768",
            temperature=0.2,
        )
        response = model.invoke(prompt)
        return response.content


llm_service = LLMService()
