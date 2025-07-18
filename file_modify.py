from settings import Settings
import psycopg2
from llm_logger import LLMLogger


settings = Settings()

logger = LLMLogger()

connection_params = {
    "host": settings.DB_HOST,
    "port": settings.DB_PORT,
    "user": settings.DB_USER,
    "password": settings.DB_PASSWORD,
    "dbname": settings.DB_NAME,
}

def ensure_modified_files_table():
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS modified_files (
        id SERIAL PRIMARY KEY,
        session_id TEXT NOT NULL,
        filename TEXT NOT NULL,
        file_type TEXT NOT NULL,
        content BYTEA,              
        data JSONB,           
        upload_time TIMESTAMPTZ DEFAULT NOW()
    );
    """
    try:
        with psycopg2.connect(**connection_params) as conn:
            with conn.cursor() as cur:
                cur.execute(create_table_sql)
        logger.info('(MCP) Ensured modified_files exists')
    except Exception as e:
        logger.error(f'(MCP) Error ensuring modified_files table: {e}')

    


