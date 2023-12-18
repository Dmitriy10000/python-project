# chats.py
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Chats(Base):
	__tablename__ = 'chats'
	chat_id = Column(Integer, primary_key=True, autoincrement=True)
	chat_name = Column(String(255), nullable=False)
	created_at = Column(Date, nullable=False)
	type = Column(String(255), nullable=False)
