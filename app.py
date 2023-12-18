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


from flask import Flask, session
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
from views.chat_views import chat_bp
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


# Регистрируем блюпринты
app.register_blueprint(auth_bp, name='auth')
app.register_blueprint(index_bp, name='index')
app.register_blueprint(add_friend_bp, name='add_friend')
app.register_blueprint(search_bp, name='search')
app.register_blueprint(chat_bp, name='chat')







# Маршрут для сообщений
@socketio.on('message')
def handle_message(msg):
	# Получаем данные пользователя
	Session = get_session()
	user_id = session.get('user_id')
	with Session as SQLSession:
		user = SQLSession.query(Users).filter(Users.user_id == user_id).first()
	# Отправляем сообщение
	print('user', user.user_id)
	print('msg', msg)
	send(msg, broadcast=True)






# Запускаем приложение
if __name__ == '__main__':
	create_database_tables()
	Session = get_session()
	app.run(debug=True)
	socketio.run(app, debug=True)

