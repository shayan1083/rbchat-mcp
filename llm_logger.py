import logging
from settings import Settings
from postgres_logging import PostgresHandler

settings = Settings()

class LLMLogger:
    def __init__(self):
        self.settings = Settings()

        self.logger = logging.getLogger("llm_logger")
        self.logger.propagate = False
        log_level = getattr(logging, self.settings.LOG_LEVEL.upper(), logging.INFO)
        self.logger.setLevel(log_level)

        self.connection_params = {
            "host": self.settings.DB_HOST,
            "port": self.settings.DB_PORT,
            "user": self.settings.DB_USER,
            "password": self.settings.DB_PASSWORD,
            "dbname": self.settings.DB_NAME,
        }

        if self.settings.ENABLE_LOGGING and not self.logger.handlers:
            pg_handler = PostgresHandler(self.connection_params)
            pg_handler.setLevel(log_level)
            self.logger.addHandler(pg_handler)


    def info(self, message: str):
        self.logger.info(message, stacklevel=2)

    def debug(self, message: str):
        self.logger.debug(message, stacklevel=2)

    def error(self, message: str):
        self.logger.error(message, stacklevel=2)

    def log_sql_output(self, sql_query: str):
        self.logger.info(f"(MCP) [SQL Query] {sql_query}", stacklevel=2)


    