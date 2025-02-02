# chat_members.py
from sqlalchemy import Column, Integer, Date, Boolean, String
from sqlalchemy.orm import declarative_base
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
import os

Base = declarative_base()
class ChatMembers(Base):
	__tablename__ = 'chat_members'
	primary_key = Column(Integer, primary_key=True)
	chat_id = Column(Integer, nullable=False)
	user_id = Column(Integer, nullable=False)
	is_admin = Column(Boolean, nullable=False)
	joined_at = Column(Date, nullable=False)
	encrypted_key = Column(String(5000), nullable=False)


	def get_symmetric_key(self, private_key):
		encrypted_key = bytes.fromhex(self.encrypted_key)
		private_key = serialization.load_pem_private_key(
			private_key.encode(),
			password=None,
		)
		print('encrypted_key', encrypted_key)
		decrypted_key = private_key.decrypt(
			encrypted_key,
			padding.OAEP(
				mgf=padding.MGF1(algorithm=hashes.SHA256()),
				algorithm=hashes.SHA256(),
				label=None
			)
		)
		return decrypted_key
	

	def __set_symmetric_key(self, symmetric_key, public_key):
		encrypted_key = public_key.encrypt(
			symmetric_key,
			padding.OAEP(
				mgf=padding.MGF1(algorithm=hashes.SHA256()),
				algorithm=hashes.SHA256(),
				label=None
			)
		)
		self.encrypted_key = encrypted_key.hex()
		return self.encrypted_key
	

	def generate_symmetric_key():
		return os.urandom(32)	# Для AES-256 используем 32 байта
	
	
	def __init__(self, chat_id, user_id, is_admin, joined_at, symmetric_key, public_key):
		public_key = serialization.load_pem_public_key(
			public_key.encode(),
		)
		self.chat_id = chat_id
		self.user_id = user_id
		self.is_admin = is_admin
		self.joined_at = joined_at
		self.encrypted_key = self.__set_symmetric_key(symmetric_key, public_key)