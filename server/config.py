from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    llm_api_key: str = ""
    llm_base_url: str = "https://api.openai.com/v1"
    llm_model: str = "gpt-4o"
    embedding_model: str = "text-embedding-3-small"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/companion"
    cors_origins: list[str] = ["http://localhost:8000", "http://localhost:3000"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
