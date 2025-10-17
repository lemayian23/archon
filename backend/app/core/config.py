from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Archon"
    API_V1_STR: str = "/api/v1"
    
    # Use SQLite for development instead of PostgreSQL
    DATABASE_URL: str = "sqlite:///./archon.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    
    class Config:
        case_sensitive = True

settings = Settings()
