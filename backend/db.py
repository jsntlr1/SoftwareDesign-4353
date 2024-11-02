import psycopg2
import os
from psycopg2 import OperationalError

def get_db_connection():
    conn = psycopg2.connect(
        host = "localhost",
        database = os.environ.get('DB_NAME', 'volunteer_management_db'),
        user=os.environ.get('DB_USER', 'postgres'),
        port = '5432'

    )
    return conn

def test_db_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database = "volunteer_management_db",
            user = "postgres",
        )

        print("Connection to db successful")

    except OperationalError as e:
        print("ERROR while connecting to db:", {e})
