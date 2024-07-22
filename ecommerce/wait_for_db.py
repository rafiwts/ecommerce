import os
import time

import psycopg2
from dotenv import load_dotenv
from psycopg2 import OperationalError

load_dotenv()


def wait_for_postgres():
    db_host = os.getenv("DATABASE_HOST", "db")
    db_port = os.getenv("DATABASE_PORT", "5432")
    db_name = os.getenv("DATABASE_NAME")
    db_user = os.getenv("USER_NAME")
    db_password = os.getenv("PASSWORD")

    while True:
        try:
            conn = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port,
            )
            conn.close()
            print("PostgreSQL is ready")
            break
        except OperationalError:
            print("PostgreSQL not available yet, waiting...")
            time.sleep(1)


if __name__ == "__main__":
    wait_for_postgres()
