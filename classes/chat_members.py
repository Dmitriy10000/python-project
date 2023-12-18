# chat_members.py
from sqlalchemy import Column, Integer, Date, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()
# darova dima eto Ivan
class ChatMembers(Base):
	__tablename__ = 'chat_members'
	chat_id = Column(Integer, nullable=False)
	user_id = Column(Integer, nullable=False)
	is_admin = Column(Boolean, nullable=False)
	joined_at = Column(Date, nullable=False)
	primary_key = Column(Integer, primary_key=True)
