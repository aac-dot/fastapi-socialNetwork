from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost/fastapi'

# Connect to database
engine = create_engine(SQLALCHEMY_DATABASE_URL)