# friends.py
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Friends(Base):
    __tablename__ = 'friends'
    user_id1 = Column(Integer, nullable=False)
    user_id2 = Column(Integer, nullable=False)
    primary_key = Column(Integer, primary_key=True)
