# users.py
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True, autoincrement=True)
	login = Column(String(255), nullable=False)
	password_hash = Column(String(255), nullable=False)
	created_at = Column(Date, nullable=False)
	email = Column(String(255), nullable=False)
	name = Column(String(255), nullable=False)
	surname = Column(String(255), nullable=False)
