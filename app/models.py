from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, text, ARRAY
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=True, server_default="TRUE")
    # rating = Column(ARRAY(Integer), nullable=True, server_default="None")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False, unique=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))