import psycopg2
from settings import Settings
from llm_logger import log_info, log_error
import uuid
from file_modify import ensure_modified_files_table

settings = Settings()

class UserRepository:
    def __init__(self):
        self.connection_params = {
            "host": settings.DB_HOST,
            "port": settings.DB_PORT,
            "user": settings.DB_USER,
            "password": settings.DB_PASSWORD,
            "dbname": settings.DB_NAME,
        }
        self.conn = None
        try:
            self.conn = psycopg2.connect(**self.connection_params)
            log_info("[UserRepository] Database connection established.")
        except Exception as e:
            log_error(f"[UserRepository] Failed to connect to database: {e}")
        
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()
            log_info("[UserRepository] Database connection closed.")

    
    def run_sql_query(self, query: str):
        log_info(f"[UserRepository] Executing SQL query: {query}")
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                col_names = [desc[0] for desc in cursor.description]
                return [dict(zip(col_names, row)) for row in rows]
        except Exception as e:
            log_error(f"[UserRepository] SQL execution failed: {e}")
            return []


    def save_binary_file_from_mcp(self, filename: str, file_type: str, content: bytes):
        ensure_modified_files_table()
        log_info('[UserRepository] Writing files into database')
        session_id = str(uuid.uuid4())
        with psycopg2.connect(**self.connection_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO modified_files (session_id, filename, file_type, content, upload_time)
                    VALUES (%s, %s, %s, %s, NOW())
                    RETURNING id;
                """, (session_id, filename, file_type, psycopg2.Binary(content)))

                file_id = cur.fetchone()[0]
        log_info('[UserRepository] File uploaded')
        return {
            "message": "File saved successfully",
            "filename": filename,
            "url": f"http://{settings.FASTAPI_HOST}:{settings.FASTAPI_PORT}/download/{file_id}"
        }
    

