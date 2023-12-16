from enum import Enum
from functools import lru_cache
from pydantic_settings import BaseSettings

class GPTModel(str, Enum):
    gpt_4 = "gpt-4"
    gpt_3_5_turbo = "gpt-3.5-turbo"

class Settings(BaseSettings):
    service_name: str = "Análisis de textos jurídicos API"
    k_revision: str = "Local"
    log_level: str = "DEBUG"
    openai_api_key: str
    model: GPTModel = GPTModel.gpt_4

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()