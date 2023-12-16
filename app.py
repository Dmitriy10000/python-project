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
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Замените на свой секретный ключ

with open('DB_cfg.json', 'r') as f:
	DB_cfg = json.load(f)

# Настройки базы данных
engine = create_engine(f"postgresql://{DB_cfg['USER']}:{DB_cfg['PASSWORD']}@{DB_cfg['HOST']}:{DB_cfg['PORT']}/{DB_cfg['DB']}")
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

Users.metadata.create_all(engine)
print('Users table created')
# Friends.metadata.create_all(engine)
# print('Friends table created')
# Invites.metadata.create_all(engine)
# print('Invites table created')
# Messages.metadata.create_all(engine)
# print('Messages table created')
# Chats.metadata.create_all(engine)
# print('Chats table created')
# ChatMembers.metadata.create_all(engine)
# print('ChatMembers table created')


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
		session = Session()
		session.add(new_user)
		session.commit()
		
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
			session['user_id'] = user.id
			flash('Вы успешно вошли в систему!', 'success')
			return redirect('/profile')
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
	user = get_logged_in_user()  # Реализуйте функцию get_logged_in_user(), которая возвращает текущего пользователя или None
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
	# user_id = session.get('user_id')
	# if user_id:
	# 	user = Session().query(Users).get(user_id)
	# 	return render_template('chat.html', user=user)
	# else:
	# 	return redirect('/login')
	return render_template('chat.html')


# Создаем маршрут для поиска пользователей
@app.route('/search', methods=['GET', 'POST'])
def search_users():
	if request.method == 'POST':
		search_query = request.form['search_query']
		users = Session().query(Users).filter(Users.login.ilike(f"%{search_query}%")).all()
		return render_template('search_results.html', users=users)

	return render_template('search.html')

if __name__ == '__main__':
	app.run(debug=True)

