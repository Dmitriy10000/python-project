# messages.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Messages(Base):
	__tablename__ = 'messages'
	
	message_id = Column(Integer, primary_key=True, autoincrement=True)
	chat_id = Column(Integer, nullable=False)
	user_id = Column(Integer, nullable=False)
	content = Column(String(255), nullable=False)
	timestamp = Column(DateTime, nullable=False)
	
	# to json
	def __repr__(self):
		return {
			'message_id': self.message_id,
			'chat_id': self.chat_id,
			'user_id': self.user_id,
			'content': self.content,
			'timestamp': self.timestamp.strftime("%d.%m.%Y %H:%M:%S"),
		}