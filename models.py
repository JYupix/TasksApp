from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from database import engine

Base = declarative_base()

class Tasks(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, nullable=False)
    body = Column(Integer, nullable=False)
    state = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)