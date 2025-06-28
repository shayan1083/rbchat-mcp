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
    DB_CHAT_HISTORY_TABLE: str = os.getenv('DB_CHAT_HISTORY_TABLE')

    MCP_SERVER_HOST: str = os.getenv('MCP_SERVER_HOST')
    MCP_SERVER_PORT: str = os.getenv('MCP_SERVER_PORT')
    MCP_SERVER_URL: str = f"http://{MCP_SERVER_HOST}:{MCP_SERVER_PORT}/mcp-server/mcp"

    ENABLE_LOGGING: bool= os.getenv('ENABLE_LOGGING')
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')