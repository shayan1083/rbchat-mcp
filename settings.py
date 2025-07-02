import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env_path = ".env"
load_dotenv(env_path)

class Settings(BaseSettings):
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: int = int(os.getenv('DB_PORT'))
    DB_USER: str = os.getenv('DB_USER')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DB_NAME: str = os.getenv('DB_NAME')

    MCP_SERVER_PORT: str = os.getenv('MCP_SERVER_PORT')
    
    ALLOWED_ORIGINS: str = os.getenv('ALLOWED_ORIGINS', '*')

    ENABLE_LOGGING: bool= os.getenv('ENABLE_LOGGING')
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')