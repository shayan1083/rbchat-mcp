from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_USER: str = 'postgres'
    DB_PASSWORD: str 
    DB_NAME: str = 'main'
    
    ALLOWED_ORIGINS: str = 'http://localhost:5173'

    ENABLE_LOGGING: bool = True
    LOG_LEVEL: str = 'INFO'
    
    GOOGLE_API_KEY: str
    CSE_ID: str
    TAVILY_API_KEY: str

    FASTAPI_HOST: str 
    FASTAPI_PORT: int

    class Config:
        env_file = ".env"
        extra = "allow"