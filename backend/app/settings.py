from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = Path(__file__).resolve().parents[2] / ".env" # parent[2] -> two folders back from current folder

class Settings(BaseSettings):
        database_url:str
        redis_url: str

        model_config = SettingsConfigDict(
                env_file=str(ENV_PATH),
                env_file_encoding="utf-8",
                extra="ignore",
        )

settings = Settings()
