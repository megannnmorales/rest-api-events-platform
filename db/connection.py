import psycopg2
import os 
from dotenv import load_dotenv

def get_connection():

    ENV = os.getenv("ENV")
    load_dotenv(f".env.{ENV}")

    if not os.getenv("PGDATABASE"):
        raise RuntimeError("PGDATABASE NOT SET")

    connection = psycopg2.connect()

    return connection