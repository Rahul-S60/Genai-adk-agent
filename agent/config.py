import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables."""

    google_api_key: str = Field(default="", alias="GOOGLE_API_KEY")
    model_name: str = Field(default="gemini-2.0-flash", alias="MODEL_NAME")
    app_name: str = Field(default="genai-learning-assistant", alias="APP_NAME")
    max_message_length: int = Field(default=8000, alias="MAX_MESSAGE_LENGTH")

    class Config:
        populate_by_name = True


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    settings = Settings()
    if not settings.google_api_key:
        raise ValueError("GOOGLE_API_KEY is not set.")

    # Make sure SDKs expecting env access can read the API key.
    os.environ["GOOGLE_API_KEY"] = settings.google_api_key
    return settings
