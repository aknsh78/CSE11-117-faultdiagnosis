import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "faultdiagnosis_db"
DB_USER = "postgres"
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


if __name__ == "__main__":
    try:
        connection = get_connection()
        print("Successfully connected to PostgreSQL!")
        connection.close()

    except Exception as e:
        print("Database connection failed:")
        print(e)