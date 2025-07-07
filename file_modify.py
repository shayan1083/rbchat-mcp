from settings import Settings
import psycopg2


settings = Settings()

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
    with psycopg2.connect(**connection_params) as conn:
        with conn.cursor() as cur:
            cur.execute(create_table_sql)


