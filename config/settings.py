import os


DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
DB_NAME = os.getenv("DB_NAME", "drone-api")
DB_HOST = os.getenv("DB_HOST", "localhost")

SQLALCHEMY_DATABASE_URI = (
    "postgresql://" + f"{DB_PASS}:{DB_USER}@{DB_HOST}/{DB_NAME}"
)
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = os.getenv("SECRET_KEY", "neO1Bhfajt")
