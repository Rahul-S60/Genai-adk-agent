from __future__ import annotations

from typing import Optional
from uuid import uuid4

from google.adk.agents.llm_agent import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types

from agent.config import get_settings
from agent.tools import explain_code
from agent.tools import summarize_text
from agent.tools import web_search


settings = get_settings()


root_agent = Agent(
    name="ai_learning_assistant",
    model=settings.model_name,
    description="An AI Learning Assistant focused on GenAI and developer learning.",
    instruction=(
        "You are an AI Learning Assistant. Help users learn AI tools, generative AI, "
        "and developer resources with practical, accurate guidance. "
        "Use tools when useful: web_search for fresh references, summarize_text for "
        "condensing content, and explain_code for code walk-throughs."
    ),
    tools=[web_search, summarize_text, explain_code],
)


class LearningAssistantService:
    """Thin service wrapper to run ADK agent requests from FastAPI."""

    def __init__(self) -> None:
        self._runner = InMemoryRunner(agent=root_agent, app_name=settings.app_name)

    async def chat(self, message: str, user_id: Optional[str] = None) -> str:
        if len(message) > settings.max_message_length:
            raise ValueError(
                f"Message is too long. Max length is {settings.max_message_length} characters."
            )

        active_user = user_id or "api-user"
        session = await self._runner.session_service.create_session(
            app_name=settings.app_name,
            user_id=active_user,
            session_id=str(uuid4()),
        )

        content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=message)],
        )

        chunks: list[str] = []
        async for event in self._runner.run_async(
            user_id=active_user,
            session_id=session.id,
            new_message=content,
        ):
            if not event.content or not event.content.parts:
                continue
            for part in event.content.parts:
                text = getattr(part, "text", None)
                if text:
                    chunks.append(text)

        response_text = "\n".join(chunks).strip()
        if not response_text:
            raise RuntimeError("Agent did not return a response.")

        return response_text
