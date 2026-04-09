from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "Astro-Oracle"
    DEBUG: bool = False
    PORT: int = 8000
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    
    # Vector Database
    CHROMA_DB_DIRECTORY: str = "./app/vectorstore"
    EMBEDDING_MODEL_NAME: str = "text-embedding-3-small"
    
    # Astrology Engine Preferences
    DEFAULT_LANGUAGE: str = "tr"
    MAPPING_SYSTEM: str = "placidus"
    ASTROLOGY_PERSPECTIVE: str = "combination"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
