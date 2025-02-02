from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Генерация пары ключей RSA
private_key = rsa.generate_private_key(
	public_exponent=65537,
	key_size=2048,
)
public_key = private_key.public_key()

# Сериализация ключей для хранения
private_key_pem = private_key.private_bytes(
	encoding=serialization.Encoding.PEM,
	format=serialization.PrivateFormat.PKCS8,
	encryption_algorithm=serialization.NoEncryption(),
)
public_key_pem = public_key.public_bytes(
	encoding=serialization.Encoding.PEM,
	format=serialization.PublicFormat.SubjectPublicKeyInfo,
)
print(f"Приватный ключ:\n{private_key_pem.decode()}")
print(f"Публичный ключ:\n{public_key_pem.decode()}")



import os

# Генерация ключа AES (16 байт = 128 бит, 32 байта = 256 бит)
symmetric_key = os.urandom(32)  # Для AES-256 используем 32 байта
print(f"Симметричный ключ: {symmetric_key.hex()}")



from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

recipient_public_key = serialization.load_pem_public_key(
	public_key_pem,
)

# Шифрование симметричного ключа
encrypted_key = recipient_public_key.encrypt(
	symmetric_key,
	padding.OAEP(
		mgf=padding.MGF1(algorithm=hashes.SHA256()),
		algorithm=hashes.SHA256(),
		label=None
	)
)

print(f"Зашифрованный симметричный ключ: {encrypted_key.hex()}")



from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

# Генерация случайного вектора инициализации (IV)
iv = os.urandom(16)

# Шифрование сообщения
cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv))
encryptor = cipher.encryptor()
ciphertext = encryptor.update(b"Your message here") + encryptor.finalize()
print(f"Зашифрованный текст: {ciphertext.hex()}")



# Расшифровка симметричного ключа
decrypted_key = private_key.decrypt(
	encrypted_key,
	padding.OAEP(
		mgf=padding.MGF1(algorithm=hashes.SHA256()),
		algorithm=hashes.SHA256(),
		label=None
	)
)

# Расшифровка сообщения
cipher = Cipher(algorithms.AES(decrypted_key), modes.CFB(iv))
decryptor = cipher.decryptor()
plaintext = decryptor.update(ciphertext) + decryptor.finalize()

print(f"Расшифрованный текст: {plaintext.decode()}")