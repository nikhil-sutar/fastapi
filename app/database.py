from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# import psycopg
# from psycopg.rows import dict_row
# import time
# while True:
#     try:
#         conn = psycopg.connect("host=localhost dbname=fastapi user=nikhil password=pass1234", row_factory=dict_row)
#         cursor = conn.cursor()
#         print("Connected to database successfully!!!")
#         break
#     except Exception as e:
#         print("Failed to connect to database...")
#         print("Error: ", e)
#         time.sleep(2)