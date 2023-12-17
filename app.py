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
import hash

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
		password = request.form['password']
		# Хэшируем пароль
		print('password', password)
		password_hash = hash.hash_password(password)
		print('password_hash', password_hash)
		is_password_valid = hash.verify_password(password, password_hash)
		print("Is Password Valid:", is_password_valid)
		db_hash = hash.convert_to_db_format(password_hash)
		print('db_hash', db_hash)
		email = request.form['email']
		name = request.form['name']
		surname = request.form['surname']
		# Проверяем, существует ли пользователь с таким логином
		existing_user = Session().query(Users).filter_by(login=login).first()
		if existing_user:
			return jsonify({'error': 'Пользователь с таким логином уже существует'})

		new_user = Users(login=login, password_hash=db_hash, created_at=datetime.now(), email=email, name=name, surname=surname)
		SQLsession = Session()
		SQLsession.add(new_user)
		SQLsession.commit()
		user = SQLsession.query(Users).filter_by(login=login).first()
		session['user_id'] = user.user_id
		return redirect('/')

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
		password = request.form['password']
		user = Session().query(Users).filter_by(login=login).first()
		user.password_hash = hash.convert_from_db_format(user.password_hash)
		is_password_valid = hash.verify_password(password, user.password_hash)
		print("Is Password Valid:", is_password_valid)
		if is_password_valid:
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
@app.route('/add_friend', methods=['POST'])
def add_friend():
	# Вывести id пользователя из сессии
	print(session.get('user_id'))
	if request.method == 'POST':
		print(request.form)
		user_id1 = session.get('user_id')
		user_id2 = request.form['user_id']
		request_type = request.form['request_type']

		# Если пользователь не авторизован, то перенаправляем на страницу входа
		if not user_id1:
			return redirect('/login')

		# Проверяем, существует ли пользователь с таким id
		existing_user = Session().query(Users).filter_by(user_id=user_id1).first()
		if not existing_user:
			print('Пользователь 1 не найден')
			return jsonify({'error': 'Пользователь 1 не найден'})
	
		# Проверяем, существует ли пользователь с таким id
		existing_user = Session().query(Users).filter_by(user_id=user_id2).first()
		if not existing_user:
			print('Пользователь 2 не найден')
			return jsonify({'error': 'Пользователь 2 не найден'})
		
		# Проверяем, не пытается ли пользователь добавить самого себя
		if int(user_id1) == int(user_id2):
			print('Нельзя добавить самого себя')
			return jsonify({'error': 'Нельзя добавить самого себя'})
		
		# Запрос в друзья
		if request_type == 'add':
			print('Запрос в друзья от', user_id1, 'к', user_id2)

			# Проверяем, не является ли пользователь другом
			existing_friend = Session().query(Friends).filter_by(user_id1=user_id1, user_id2=user_id2).first()
			if existing_friend:
				print('Пользователь уже является другом')
				return jsonify({'error': 'Пользователь уже является другом'})
			
			# Проверяем, не было ли уже отправлено приглашение
			existing_invite = Session().query(Invites).filter_by(user_id1=user_id1, user_id2=user_id2).first()
			if existing_invite:
				print('Приглашение уже отправлено')
				return jsonify({'error': 'Приглашение уже отправлено'})
			
			# Проверяем, не было ли уже получено приглашение
			existing_invite = Session().query(Invites).filter_by(user_id1=user_id2, user_id2=user_id1).first()
			if existing_invite:
				# Добавляем в друзья user_id1 меньше user_id2
				print('Приглашение уже получено, добавляем в друзья')
				new_friend = Friends(user_id1=min(user_id1, user_id2), user_id2=max(user_id1, user_id2))
				SQLsession = Session()
				SQLsession.add(new_friend)
				SQLsession.commit()
				print('Пользователь успешно добавлен в друзья')

				# Удаляем приглашение
				SQLsession.query(Invites).filter_by(user_id1=user_id2, user_id2=user_id1).delete()
				SQLsession.commit()
				print('Приглашение удалено')
				return jsonify({'success': 'Пользователь успешно добавлен в друзья'})
			
			# Если приглашение не было отправлено и не было получено, то отправляем приглашение
			print('Отправляем приглашение')
			new_invite = Invites(user_id1=user_id1, user_id2=user_id2)
			SQLsession = Session()
			SQLsession.add(new_invite)
			SQLsession.commit()
			print('Приглашение успешно отправлено')
			return jsonify({'success': 'Приглашение успешно отправлено'})
		
		# Удаление из друзей
		elif request_type == 'delete':
			print('Удаление из друзей', user_id1, 'к', user_id2)
			# Проверяем, является ли пользователь другом
			existing_friend = Session().query(Friends).filter_by(user_id1=user_id1, user_id2=user_id2).first()
			if not existing_friend:
				print('Пользователь не является другом')
				return jsonify({'error': 'Пользователь не является другом'})
			
			# Удаляем из друзей
			SQLsession = Session()
			SQLsession.query(Friends).filter_by(user_id1=user_id1, user_id2=user_id2).delete()
			SQLsession.commit()
			print('Пользователь успешно удален из друзей')
			return jsonify({'success': 'Пользователь успешно удален из друзей'})
		
		# Отмена приглашения
		elif request_type == 'cancel':
			print('Отмена приглашения', user_id1, 'к', user_id2)
			
			# Проверяем, было ли отправлено приглашение
			existing_invite = Session().query(Invites).filter_by(user_id1=user_id1, user_id2=user_id2).first()
			if not existing_invite:
				print('Приглашение не было отправлено')
				return jsonify({'error': 'Приглашение не было отправлено'})
			
			# Удаляем приглашение
			SQLsession = Session()
			SQLsession.query(Invites).filter_by(user_id1=user_id1, user_id2=user_id2).delete()
			SQLsession.commit()
			print('Приглашение успешно отменено')
			return jsonify({'success': 'Приглашение успешно отменено'})
		
		# Отклонение приглашения
		elif request_type == 'decline':
			print('Отклонение приглашения', user_id1, 'к', user_id2)
			# Проверяем, было ли получено приглашение
			existing_invite = Session().query(Invites).filter_by(user_id1=user_id2, user_id2=user_id1).first()
			if not existing_invite:
				print('Приглашение не было получено')
				return jsonify({'error': 'Приглашение не было получено'})
			
			# Удаляем приглашение
			SQLsession = Session()
			SQLsession.query(Invites).filter_by(user_id1=user_id2, user_id2=user_id1).delete()
			SQLsession.commit()
			print('Приглашение успешно отклонено')
			return jsonify({'success': 'Приглашение успешно отклонено'})
		
		# Принятие приглашения
		elif request_type == 'accept':
			print('Принятие приглашения', user_id1, 'к', user_id2)
			# Проверяем, было ли получено приглашение
			existing_invite = Session().query(Invites).filter_by(user_id1=user_id2, user_id2=user_id1).first()
			if not existing_invite:
				print('Приглашение не было получено')
				return jsonify({'error': 'Приглашение не было получено'})
			
			# Проверяем, не является ли пользователь другом
			existing_friend = Session().query(Friends).filter_by(user_id1=user_id1, user_id2=user_id2).first()
			if existing_friend:
				print('Пользователь уже является другом')
				return jsonify({'error': 'Пользователь уже является другом'})
			
			# Добавляем в друзья
			new_friend = Friends(user_id1=user_id1, user_id2=user_id2)
			SQLsession = Session()
			SQLsession.add(new_friend)
			SQLsession.commit()
			print('Пользователь успешно добавлен в друзья')

			# Удаляем приглашение
			SQLsession.query(Invites).filter_by(user_id1=user_id2, user_id2=user_id1).delete()
			SQLsession.commit()
			print('Приглашение удалено')
			return jsonify({'success': 'Пользователь успешно добавлен в друзья'})
	
	return redirect('/search')


# Принимаем ajax запрос на получение списка друзей и возвращаем json
@app.route('/global_user_search', methods=['POST'])
def global_user_search():
	print(request.form)
	search_query = request.form['search_query']

	# Проверяем запрос на пустоту
	if search_query == '':
		return jsonify({'error': 'Пустой запрос'})
	
	# Ищем пользователей по запросу
	users = Session().query(Users).filter(Users.login.ilike(f"%{search_query}%")).all()

	# Удаляем из списка текущего пользователя
	user_id = session.get('user_id')
	for user in users:
		if user.user_id == user_id:
			users.remove(user)
			break			

	# Пакуем данные в json и отправляем
	users_json = []
	for user in users:
		# Проверяем, не являются ли пользователи друзьями
		# user_id1 меньше user_id2
		exiting_friend = Session().query(Friends).filter_by(user_id1=min(user_id, user.user_id), user_id2=max(user_id, user.user_id)).first()
		if exiting_friend:
			users_json.append({'user_id': user.user_id, 'login': user.login, 'name': user.name, 'surname': user.surname, 'is_friend': True})
			continue

		# Проверяем, не было ли отправлено исходящее приглашение
		existing_invite = Session().query(Invites).filter_by(user_id1=user_id, user_id2=user.user_id).first()
		if existing_invite:
			users_json.append({'user_id': user.user_id, 'login': user.login, 'name': user.name, 'surname': user.surname, 'is_invite_sent': True})
			continue

		# Проверяем, не было ли получено входящее приглашение
		existing_invite = Session().query(Invites).filter_by(user_id1=user.user_id, user_id2=user_id).first()
		if existing_invite:
			users_json.append({'user_id': user.user_id, 'login': user.login, 'name': user.name, 'surname': user.surname, 'is_invite_received': True})
			continue

		# Если ничего не найдено, то добавляем пользователя в список
		users_json.append({'user_id': user.user_id, 'login': user.login, 'name': user.name, 'surname': user.surname, 'is_friend': False})
	return jsonify(users_json)


if __name__ == '__main__':
	app.run(debug=True)

