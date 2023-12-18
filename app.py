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


from flask import Flask, request, session
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
	# Получаем данные пользователя
	user_id = session.get('user_id')
	with Session as SQLSession:
		user = SQLSession.query(Users).filter(Users.user_id == user_id).first()
		need_chat_id = user_in_chat[user.user_id]
		
		# debug
		print('aboboaobaobaobaoboa', user_in_chat)
		print('Входящее сообщение от пользователя с id', user.user_id, 'содержание:', msg)
		
		# Записываем сообщение в бд
		try:
			message = Messages(user_id=user.user_id, chat_id=user_in_chat[user.user_id], content=msg['message'], timestamp=datetime.now())
			SQLSession.add(message)
			SQLSession.commit()
		except Exception as e:
			print('Ошибка при записи сообщения в бд', e)

		# Отправляем сообщение всем участникам чата, которые находятся во вкладке чата, совпадающей с чатом, в котором было отправлено сообщение
		print('user_in_chat', user_in_chat)
		for user_id in user_in_chat:
			print('user_id', user_id)
			print('need_chat_id', need_chat_id)
			print('user_in_chat[user_id]', user_in_chat[user_id])

			# Пропускаем пользователей, которые не находятся во вкладке чата, совпадающей с чатом, в котором было отправлено сообщение
			if user_in_chat[user_id] != need_chat_id:
				continue
			
			# Получаем имя и фамилию пользователя, который отправил сообщение
			with Session as SQLSession:
				user = SQLSession.query(Users).filter(Users.user_id == user_id).first()

			# Пакуем сообщение в json
			data = {
				'user_id': user.user_id,
				'target_id': user_id,
				'chat_id': need_chat_id,
				'chat_name': user.name + ' ' + user.surname,
				'timestamp': datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
				'message': msg,
			}

			# Отправляем сообщение
			print('Отправляем сообщение', data, 'в комнату', user_in_socket[user_id])
			emit('message', data, room=user_in_socket[user_id])
				

# Инициализируем сокеты
@socketio.on('connect')
def test_connect():
	print('Client connected')
	user_id = session.get('user_id')
	user_in_socket[user_id] = request.sid
	print('user_in_socket', user_in_socket)


# Запускаем приложение
if __name__ == '__main__':
	create_database_tables()
	Session = get_session()
	app.run(debug=True)
	socketio.run(app, debug=True)
