import logging
from settings import Settings
from postgres_logging import PostgresHandler

settings = Settings()

logger = logging.getLogger("llm_logger")
logger.handlers.clear()

log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
logger.setLevel(log_level)
logger.propagate = False

connection_params = {
            "host": settings.DB_HOST,
            "port": settings.DB_PORT,
            "user": settings.DB_USER,
            "password": settings.DB_PASSWORD,
            "dbname": settings.DB_NAME,
        }


def log_info(message: str):
    logger.info(f"{message}", stacklevel=2)

def log_error(message: str):
    logger.error(f"{message}", exc_info=True, stacklevel=2)

def log_sql_output(sql_query: str):
    logger.info(f"[SQL Query] {sql_query}", stacklevel=2)

# Main usage logging
def log_llm_usage(model_name: str, prompt: str, response: str, token_usage: dict, tool_used: str = None):
    logger.info(f"[LLM] Model: {model_name}", stacklevel=2)
    logger.info(f"[LLM] Prompt: {prompt}", stacklevel=2)
    logger.info(f"[LLM] Response: {response}", stacklevel=2)
    logger.info(
        f"[Usage] Tokens - Input: {token_usage.get('input_tokens')}, "
        f"Output: {token_usage.get('output_tokens')}, "
        f"Total: {token_usage.get('total_tokens')}"
    )

if settings.ENABLE_LOGGING:
    pg_handler = PostgresHandler(connection_params)
    pg_handler.setLevel(log_level)
    logger.addHandler(pg_handler)
