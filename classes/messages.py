# messages.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

Base = declarative_base()

class Messages(Base):
	__tablename__ = 'messages'
	message_id = Column(Integer, primary_key=True, autoincrement=True)
	chat_id = Column(Integer, nullable=False)
	user_id = Column(Integer, nullable=False)
	content = Column(String(10000), nullable=False)
	iv = Column(String(255), nullable=False)
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
	

	def __init__(self, chat_id, user_id, content, timestamp):
		self.chat_id = chat_id
		self.user_id = user_id
		self.content = content
		self.timestamp = timestamp


	def get_message_id(self):
		return self.message_id
	

	def get_chat_id(self):
		return self.chat_id
	

	def	get_user_id(self):
		return self.user_id
	

	def get_content(self):
		return self.content
	

	def	get_iv(self):
		return self.iv
	

	def get_timestamp(self):
		return self.timestamp.strftime("%d.%m.%Y %H:%M:%S")


	def encrypt_message(self, symmetric_key):
		msg = self.content
		print('msg', msg)
		print('message.encode()', msg.encode())
		self.iv = os.urandom(16)
		print('self.iv', self.iv)
		# Шифрование сообщения
		cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(self.iv))
		self.iv = self.iv
		encryptor = cipher.encryptor()
		ciphertext = encryptor.update(msg.encode()) + encryptor.finalize()
		self.content = ciphertext.hex()
		return ciphertext
	

	def decrypt_message(self, symmetric_key):
		self.iv = bytes.fromhex(self.iv[2:])
		print('iv', self.iv)
		print('symmetric_key', symmetric_key)
		ciphertext = bytes.fromhex(self.content)
		print('ciphertext', ciphertext)
		print('ciphertext.encode()', ciphertext)
		# Расшифровка сообщения
		cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(self.iv))
		decryptor = cipher.decryptor()
		plaintext = decryptor.update(ciphertext) + decryptor.finalize()
		return plaintext.decode()