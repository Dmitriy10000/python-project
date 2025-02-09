# Сайт мессенджер на python с использованием бд PostgreSQL.
# Так же в проекте должно присутствовать:
# ООП
# Error handling
# API
# Логирование
# Сокеты
# Flask
# cryptography
# SQLAlchemy


from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, send, emit
from utils.db_manager import create_database_tables, get_session
from classes.users import Users
from classes.chats import Chats
from classes.chat_members import ChatMembers
from classes.messages import Messages
from views.auth_views import auth_bp
from views.index_views import index_bp
from views.add_friend_views import add_friend_bp
from views.search_views import search_bp
from views.chat_views import chat_bp, user_in_chat
from datetime import datetime
import logging
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


# Сохраняем логи в папку logs с названием в виде даты
path = os.path.dirname(os.path.abspath(__file__))
if not os.path.exists(f'{path}/logs'):
	os.makedirs(f'{path}/logs')
logging.basicConfig(filename=f'{path}/logs/' + datetime.now().strftime("%Y-%m-%d") + '.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


# Настройки приложения
app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)
Session = get_session()


# Регистрируем блюпринты
app.register_blueprint(auth_bp, name='auth')
app.register_blueprint(index_bp, name='index')
app.register_blueprint(add_friend_bp, name='add_friend')
app.register_blueprint(search_bp, name='search')
app.register_blueprint(chat_bp, name='chat')


user_in_socket = {}


# Маршрут для сообщений
@socketio.on('message')
def handle_message(msg):
	print(request.sid)
	# Получаем данные текущего пользователя
	user_id = session.get('user_id')
	with Session as SQLSession:
		tmp_time = datetime.now()
		user = SQLSession.query(Users).filter(Users.user_id == user_id).first()
		need_chat_id = user_in_chat[user_id]
		target = SQLSession.query(ChatMembers).filter(ChatMembers.chat_id == need_chat_id).filter(ChatMembers.user_id != user_id).first()

		
		# debug
		print('user_in_chat', user_in_chat)
		print('Входящее сообщение от пользователя с id', user_id, 'содержание:', msg)
		
		# Записываем сообщение в бд
		try:
			chat_member = SQLSession.query(ChatMembers).filter(ChatMembers.chat_id == need_chat_id).filter(ChatMembers.user_id == user_id).first()
			symmetric_key = ChatMembers.get_symmetric_key(chat_member, user.get_private_key())
			print('msg', msg['message'])
			message = Messages(user_id=user_id, chat_id=user_in_chat[user_id], content=msg['message'], timestamp=tmp_time)
			ciphertext = message.encrypt_message(symmetric_key)
			print('ciphertext', ciphertext)
			SQLSession.add(message)
			SQLSession.commit()
			# Получаем сообщение
			temp_message = SQLSession.query(Messages).filter(Messages.user_id == user_id).filter(Messages.timestamp == tmp_time).first()
		except Exception as e:
			print('Ошибка при записи сообщения в бд', e)


		# Отправляем сообщение всем участникам чата, которые находятся во вкладке чата, совпадающей с чатом, в котором было отправлено сообщение
		print('user_in_chat', user_in_chat)
		for usr_id in user_in_chat:
			print('user_id', usr_id)
			print('need_chat_id', need_chat_id)
			print('user_in_chat[user_id]', user_in_chat[usr_id])

			# Пропускаем пользователей, которые не находятся во вкладке чата, совпадающей с чатом, в котором было отправлено сообщение
			if user_in_chat[usr_id] != need_chat_id:
				continue
			
			# Получаем имя и фамилию пользователя, который отправил сообщение
			with Session as SQLSession:
				user = SQLSession.query(Users).filter(Users.user_id == user_id).first()


			# Пакуем сообщение в json
			data = {
				'user_id': user_id,
				'user_name': user.get_name() + ' ' + user.get_surname(),
				'message_id': temp_message.get_message_id(),
				# temp_message.get_content() - зашифрованное сообщение
				# msg['message'] - расшифрованное сообщение
				'content': msg['message'],
				'timestamp': temp_message.timestamp.strftime("%d.%m.%Y %H:%M:%S"),
			}

			# Отправляем сообщение
			print('Отправляем сообщение', data, 'в комнату', user_in_socket[usr_id])
			emit('message', data, room=user_in_socket[usr_id])
				

# Инициализируем сокеты
@socketio.on('connect')
def test_connect():
	print('Client connected')
	user_id = session.get('user_id')
	user_in_socket[user_id] = request.sid
	print('user_in_socket', user_in_socket)


@app.route('/error')
def error():
	return render_template('error.html')


# Запускаем приложение
if __name__ == '__main__':
	create_database_tables()
	Session = get_session()
	app.run(debug=True)
	socketio.run(app, debug=True)
