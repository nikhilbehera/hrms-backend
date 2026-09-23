from sqlalchemy import create_engine, String, Integer
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
import os


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind = engine)

class Base(DeclarativeBase):
    pass


