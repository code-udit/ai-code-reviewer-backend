from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# load env variables
load_dotenv()

# get DB URL from env
DATABASE_URL = os.getenv("DATABASE_URL")

# basic safety (prevents crash if missing)
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env")

# create engine
engine = create_engine(DATABASE_URL)

# session factory
SessionLocal = sessionmaker(bind=engine)

# base model
Base = declarative_base()