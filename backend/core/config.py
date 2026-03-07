from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    gemini_api_key: str = "default_api_key"
    page_index_api_key: str = "default_api_key"
    gemini_model: str = "default_model"

    class Config:
        env_file = ".env"

settings = Settings()
