from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv

load_dotenv()

# Local
DATABASE_URL = os.getenv("DATABASE_LOCAL")

# # Docker
# DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_connection():
    try:
        with engine.connect() as connection:
            print("Successfully connected to database")
    except Exception as e:
        print(f"An error occurred: {e}")


test_connection()
