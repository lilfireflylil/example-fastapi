from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


# SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost:port/database_name"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# "the below code is only as reference in case for not
#  using SQLAlchemy."

""" 
import psycopg2
from psycopg2.extras import RealDictCursor
import time


while True:
    try:
        conn = psycopg2.connect(
            database="fastapi",
            host="localhost",
            user="postgres",
            password="admin",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("connecting to database was successful")
        break
    except Exception as error:
        print("connecting to database failed")
        print("error: ", error)
        time.sleep(2)


"""
