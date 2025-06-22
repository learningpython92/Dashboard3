# backend/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

# Get the database URL from environment variables, with a fallback to a local SQLite file.
# This part from your code is excellent.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dashboard.db")

# --- START: NECESSARY FIXES FOR PRODUCTION ---

# This variable will hold the final, corrected URL.
SQLALCHEMY_DATABASE_URL = DATABASE_URL

# Fix 1: Render's database URLs start with "postgres://", but SQLAlchemy needs "postgresql://".
# This check handles that conversion automatically if we're in production.
if DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Fix 2: The `connect_args` is only for SQLite. We create a dictionary for it here.
connect_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# --- END: NECESSARY FIXES FOR PRODUCTION ---


# Now, we create the engine using our corrected variables.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()