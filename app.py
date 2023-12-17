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
# 
# Функции мессенджера:
# Слева страницы должен быть список контактов, нажимая на который в правой части страницы открывается диалог с этим контактом, куда можно писать и получать сообщения.
# Так же в левой части страницы можно будет нажать на иконку друзья, что бы перейти на вкладку добавления друзей
# Напиши для меня код веб приложения


from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from classes.users import Users
from classes.friends import Friends
from classes.invites import Invites
from classes.messages import Messages
from classes.chats import Chats
from classes.chat_members import ChatMembers
import logging
import json
import os

# Сохраняем логи в папку logs с названием в виде даты
path = os.path.dirname(os.path.abspath(__file__))
if not os.path.exists(f'{path}/logs'):
	os.makedirs(f'{path}/logs')
logging.basicConfig(filename=f'{path}/logs/' + datetime.now().strftime("%Y-%m-%d") + '.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__)
app.secret_key = os.urandom(24)

with open('DB_cfg.json', 'r') as f:
	DB_cfg = json.load(f)

# Настройки базы данных
engine = create_engine(f"postgresql://{DB_cfg['USER']}:{DB_cfg['PASSWORD']}@{DB_cfg['HOST']}:{DB_cfg['PORT']}/{DB_cfg['DB']}")
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

Users.metadata.create_all(engine)
print('Users table created')
Friends.metadata.create_all(engine)
print('Friends table created')
Invites.metadata.create_all(engine)
print('Invites table created')
Messages.metadata.create_all(engine)
print('Messages table created')
Chats.metadata.create_all(engine)
print('Chats table created')
ChatMembers.metadata.create_all(engine)
print('ChatMembers table created')


# Маршрут для создания пользователя
@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		login = request.form['login']
		password_hash = request.form['password_hash']
		email = request.form['email']
		name = request.form['name']
		surname = request.form['surname']

		# Проверяем, существует ли пользователь с таким логином
		existing_user = Session().query(Users).filter_by(login=login).first()
		if existing_user:
			return jsonify({'error': 'Пользователь с таким логином уже существует'})

		new_user = Users(login=login, password_hash=password_hash, created_at=datetime.now(), email=email, name=name, surname=surname)
		SQLsession = Session()
		SQLsession.add(new_user)
		SQLsession.commit()

		
		return redirect('/profile')

	return render_template('register.html')


# Маршрут для проверки доступности логина
@app.route('/check_login_availability', methods=['POST'])
def check_login_availability():
	if request.method == 'POST':
		login = request.form['login']

		existing_user = Session().query(Users).filter_by(login=login).first()
		if existing_user:
			return jsonify({'available': False})
		else:
			return jsonify({'available': True})


# Маршрут для отображения формы входа
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		login = request.form['login']
		password_hash = request.form['password_hash']

		user = Session().query(Users).filter_by(login=login, password_hash=password_hash).first()

		if user:
			# Успешный вход, устанавливаем пользователя в сессию
			session['user_id'] = user.user_id
			flash('Вы успешно вошли в систему!', 'success')
			return redirect('/')
		else:
			# Неправильный логин или пароль, выводим сообщение об ошибке
			flash('Неправильный логин или пароль. Пожалуйста, попробуйте снова.', 'error')

	# При ошибке или если пользователь не вошел, возвращаемся на страницу входа
	return render_template('login.html')


# Маршрут для отображения страницы профиля
@app.route('/profile')
def profile():
	user_id = session.get('user_id')

	if user_id:
		user = Session().query(Users).get(user_id)
		return render_template('profile.html', user=user)

	return redirect('/login')


# Маршрут для отображения домашней страницы
@app.route('/')
def home():
	user = get_logged_in_user()  # Функцию get_logged_in_user(), которая возвращает текущего пользователя или None
	return render_template('index.html', user=user)


# Функция для получения текущего пользователя из сессии
def get_logged_in_user():
	user_id = session.get('user_id')
	if user_id:
		return Session().query(Users).get(user_id)
	return None


# Маршрут для выхода из аккаунта
@app.route('/logout', methods=['POST'])
def logout():
	session.clear()
	return redirect('/')


# Маршрут для чата
@app.route('/chat', methods=['GET', 'POST'])
def chat():
	user_id = session.get('user_id')
	if user_id:
		user = Session().query(Users).get(user_id)
		return render_template('chat.html', user=user)
	else:
		return redirect('/login')
	# return render_template('chat.html')


# Создаем маршрут для поиска пользователей
@app.route('/search', methods=['GET', 'POST'])
def search_users():
	if request.method == 'POST':
		print(request.form)
		search_query = request.form['search']
		users = Session().query(Users).filter(Users.login.ilike(f"%{search_query}%")).all()
		return render_template('search.html', users=users)

	return render_template('search.html')


# Создаем маршрут для добавления друзей
@app.route('/add_user', methods=['POST'])
def add_user():
	# Вывести id пользователя из сессии
	print(session.get('user_id'))
	if request.method == 'POST':
		print(request.form)
		if request.form['type'] == 'add':
			print(session)
			print(session.get('user_id'))
			user_id1 = session.get('user_id')
			print(user_id1)
			user_id2 = request.form['user_id']
			print('Запрос в друзья от', user_id1, 'к', user_id2)
			# Проверяем, существует ли пользователь с таким логином
			existing_user = Session().query(Users).filter_by(user_id=user_id1).first()
			if existing_user:
				# Проверяем, не пытается ли пользователь добавить самого себя
				if user_id1 == user_id2:
					print('Нельзя добавить самого себя')
				else:
					# Проверяем, не является ли пользователь другом
					existing_friend = Session().query(Friends).filter_by(user_id1=user_id1, user_id2=user_id2).first()
					if existing_friend:
						print('Пользователь уже является другом')
					else:
						# Проверяем, не было ли уже отправлено приглашение
						existing_invite = Session().query(Invites).filter_by(user_id1=user_id1, user_id2=user_id2).first()
						if existing_invite:
							print('Приглашение уже отправлено')
						else:
							# Проверяем, не было ли уже получено приглашение
							existing_invite = Session().query(Invites).filter_by(user_id1=user_id2, user_id2=user_id1).first()
							if existing_invite:
								print('Приглашение уже получено, добавляем в друзья')
								new_friend = Friends(user_id1=user_id2, user_id2=user_id1)
								SQLsession = Session()
								SQLsession.add(new_friend)
								SQLsession.commit()
								print('Пользователь успешно добавлен в друзья')
								# Удаляем приглашение
								SQLsession.query(Invites).filter_by(user_id1=user_id2, user_id2=user_id1).delete()
								SQLsession.commit()
								print('Приглашение удалено')
							else:
								print('Отправляем приглашение')
								print('user_id', user_id1)
								print('friend_id', user_id2)
								print('datetime.now()', datetime.now())
								new_invite = Invites(user_id1=user_id1, user_id2=user_id2)
								SQLsession = Session()
								SQLsession.add(new_invite)
								SQLsession.commit()
								print('Приглашение успешно отправлено')
			else:
				print('Пользователь не найден')
	return redirect('/search')

if __name__ == '__main__':
	app.run(debug=True)

