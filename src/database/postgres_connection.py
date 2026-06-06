import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine


def get_postgres_engine():
    """Create and return a PostgreSQL SQLAlchemy engine."""

    env_path = Path(__file__).resolve().parents[2] / ".env"
    load_dotenv(dotenv_path=env_path, override=True)

    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    database = os.getenv("POSTGRES_DB")

    if not all([user, password, host, port, database]):
        raise ValueError("Missing PostgreSQL environment variables. Check your .env file.")

    connection_url = (
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    )

    print("=" * 50)
    print("ENV FILE:", env_path)
    print("USER:", user)
    print("HOST:", host)
    print("PORT:", port)
    print("DATABASE:", database)
    print("=" * 50)

    return create_engine(connection_url)