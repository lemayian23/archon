from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Settings(BaseSettings):
    PROJECT_NAME: str = "Archon"
    API_V1_STR: str = "/api/v1"
    
    # Use SQLite for development
    DATABASE_URL: str = "sqlite:///./archon.db"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "archon-secret-key-2024")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    class Config:
        case_sensitive = True

settings = Settings()
