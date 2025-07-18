import psycopg2
from settings import Settings
from llm_logger import LLMLogger
import uuid


settings = Settings()

logger = LLMLogger()

class UserRepository:
    def __init__(self, db_name: str = settings.DB_NAME):
        self.connection_params = {
            "host": settings.DB_HOST,
            "port": settings.DB_PORT,
            "user": settings.DB_USER,
            "password": settings.DB_PASSWORD,
            "dbname": db_name,
        }
        self.conn = None
        try:
            self.conn = psycopg2.connect(**self.connection_params)
            logger.info("(MCP) Database connection established.")
        except Exception as e:
            logger.error(f"(MCP) Failed to connect to database: {e}")
        
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()
            logger.info("(MCP) Database connection closed.")

    
    def run_sql_query(self, query: str):
        logger.info(f"(MCP) Executing SQL query: {query}")
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                col_names = [desc[0] for desc in cursor.description]
                return [dict(zip(col_names, row)) for row in rows]
        except Exception as e:
            logger.error(f"(MCP) SQL execution failed: {e}")
            return []


    def save_binary_file_from_mcp(self, filename: str, file_type: str, content: bytes):
        logger.info('(MCP) Writing files into database')
        session_id = str(uuid.uuid4())
        with psycopg2.connect(**self.connection_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO modified_files (session_id, filename, file_type, content, upload_time)
                    VALUES (%s, %s, %s, %s, NOW())
                    RETURNING id;
                """, (session_id, filename, file_type, psycopg2.Binary(content)))

                file_id = cur.fetchone()[0]
        logger.info('(MCP) File uploaded')
        return {
            "message": "File saved successfully",
            "filename": filename,
            "url": f"http://{settings.FASTAPI_HOST}:{settings.FASTAPI_PORT}/download/{file_id}"
        }
    

