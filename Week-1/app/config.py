import os

class Config:
    # SQLite database file stored in the project root
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "..", "library.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "library-secret-key-2026"
