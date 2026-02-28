import os
from urllib.parse import quote_plus

# Optionally load environment variables from a .env file for local development
try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    # dotenv is optional at runtime; it's included in requirements.txt for dev use
    pass


class Config:
    # Read DB connection values from environment with sensible defaults for local dev.
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "pallavi@2004")
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", "3306")
    DB_NAME = os.environ.get("DB_NAME", "userdetail")

    # Quote the password so characters like @, :, / don't break the URI
    quoted_password = quote_plus(DB_PASSWORD)

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{quoted_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False