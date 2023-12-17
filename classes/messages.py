# messages.py
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Messages(Base):
	__tablename__ = 'messages'
	message_id = Column(Integer, primary_key=True, autoincrement=True)
	chat_id = Column(Integer, nullable=False)
	user_id = Column(Integer, nullable=False)
	content = Column(String(255), nullable=False)
	timestamp = Column(Date, nullable=False)
