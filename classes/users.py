# users.py
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import secrets

Base = declarative_base()

class Users(Base):
	__tablename__ = 'users'
	user_id = Column(Integer, primary_key=True, autoincrement=True)
	login = Column(String(255), nullable=False)
	password_hash = Column(String(255), nullable=False)
	created_at = Column(Date, nullable=False)
	email = Column(String(255), nullable=False)
	name = Column(String(255), nullable=False)
	surname = Column(String(255), nullable=False)


	def __hash_password(password):
		# Генерация случайной соли в виде байтов
		salt = secrets.token_bytes(16)

		# Создание объекта для PBKDF2 с использованием SHA-256
		kdf = PBKDF2HMAC(
			algorithm=hashes.SHA256(),
			iterations=100000,
			length=32,
			salt=salt,
			backend=default_backend()
		)

		# Производство ключа (хэша) из пароля
		key = kdf.derive(password.encode('utf-8'))

		# Возврат хэша и соли в виде байтов
		return salt + key


	def __verify_password(input_password, stored_password):
		# Извлечение соли из хэша в виде байтов
		salt = stored_password[:16]

		# Создание объекта для PBKDF2 с использованием SHA-256
		kdf = PBKDF2HMAC(
			algorithm=hashes.SHA256(),
			iterations=100000,
			length=32,
			salt=salt,
			backend=default_backend()
		)

		# Производство ключа (хэша) из введенного пароля
		key = kdf.derive(input_password.encode('utf-8'))

		# Сравнение хэшированных паролей
		return stored_password[16:] == key


	def __convert_to_db_format(byte_hash):
		# Преобразование байтового хэша в шестнадцатеричное представление строки
		hex_hash = byte_hash.hex()
		return hex_hash


	def __convert_from_db_format(db_format_hash):
		# Преобразование строки в байтовый хэш
		byte_hash = bytes.fromhex(db_format_hash)
		return byte_hash
	

	def is_password_valid(self, input_password):
		# Преобразование хэша в байтовый формат
		byte_hash = Users.__convert_from_db_format(self.password_hash)

		# Проверка пароля
		is_password_valid = Users.__verify_password(input_password, byte_hash)
		return is_password_valid
	

	def set_password_hash_from_password(self, password):
		# Хэширование пароля
		password_hash = Users.__hash_password(password)

		# Преобразование хэша в строковый формат
		db_hash = Users.__convert_to_db_format(password_hash)
		self.password_hash = db_hash
		return self.password_hash
