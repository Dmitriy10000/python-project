from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import secrets


def hash_password(password):
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


def verify_password(input_password, stored_password):
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


def convert_to_db_format(byte_hash):
	# Преобразование байтового хэша в шестнадцатеричное представление строки
	hex_hash = byte_hash.hex()
	return hex_hash


def convert_from_db_format(db_format_hash):
	# Преобразование строки в байтовый хэш
	byte_hash = bytes.fromhex(db_format_hash)
	return byte_hash
