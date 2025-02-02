from flask import Blueprint, render_template, redirect, flash, request, session, jsonify
from utils.db_manager import get_session
from datetime import datetime
from classes.users import Users
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


auth_bp = Blueprint('auth', __name__)
Session = get_session()


# Маршрут для отображения формы входа
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		login = request.form['login']
		password = request.form['password']
		with get_session() as SQLsession:
			user = SQLsession.query(Users).filter_by(login=login).first()
			if not user:
				flash('Неправильный логин или пароль. Пожалуйста, попробуйте снова.', 'error')
				print('Пользователь', login, 'не существует')
				return redirect('/login')

			# Успешный вход, устанавливаем пользователя в сессию
			if user and user.is_password_valid(password):
				session['user_id'] = user.user_id
				flash('Вы успешно вошли в систему!', 'success')
				print('Пользователь', user.login, 'вошел в систему')
				return redirect('/chat')

			# Неправильный логин или пароль, выводим сообщение об ошибке
			else:
				flash('Неправильный логин или пароль. Пожалуйста, попробуйте снова.', 'error')
				print('Пользователь', user.login, 'ввел неправильный пароль')
				return redirect('/login')

	# При ошибке или если пользователь не вошел, возвращаемся на страницу входа
	return render_template('login.html')


# Маршрут для проверки доступности логина
@auth_bp.route('/check_login_availability', methods=['POST'])
def check_login_availability():
	if request.method == 'POST':
		login = request.form['login']
		with Session as SQLsession:
			existing_user = SQLsession.query(Users).filter_by(login=login).first()
			if existing_user:
				return jsonify({'available': False})

			else:
				return jsonify({'available': True})


# Маршрут для создания пользователя
@auth_bp.route('/register', methods=['POST'])
def register():
	if request.method == 'POST':
		login = request.form['r_login']

		# Проверяем, существует ли пользователь с таким логином
		with Session as SQLsession:
			existing_user = SQLsession.query(Users).filter_by(login=login).first()
			if existing_user:
				return render_template('error.html', error='Пользователь с таким логином уже существует')
		
		user = Users(login=login, password=request.form['password'], email=request.form['email'], name=request.form['name'], surname=request.form['surname'])
		# password = request.form['password']
		# email = request.form['email']
		# name = request.form['name']
		# surname = request.form['surname']

		# # Генерация пары ключей RSA
		# private_key = rsa.generate_private_key(
		# 	public_exponent=65537,
		# 	key_size=2048,
		# )
		# public_key = private_key.public_key()

		# # Сериализация ключей для хранения
		# private_key_pem = private_key.private_bytes(
		# 	encoding=serialization.Encoding.PEM,
		# 	format=serialization.PrivateFormat.PKCS8,
		# 	encryption_algorithm=serialization.NoEncryption(),
		# )
		# public_key_pem = public_key.public_bytes(
		# 	encoding=serialization.Encoding.PEM,
		# 	format=serialization.PublicFormat.SubjectPublicKeyInfo,
		# )
		# print(f"Private key:\n{private_key_pem.decode()}")
		# print(f"Public key:\n{public_key_pem.decode()}")
		with Session as SQLsession:
			# new_user = Users(login=login, password_hash=password, created_at=datetime.now(), email=email, name=name, surname=surname, public_key=str(public_key_pem.decode()), private_key=str(private_key_pem.decode()))
			# new_user.set_password_hash_from_password(password)
			SQLsession.add(user)
			SQLsession.commit()
			user = SQLsession.query(Users).filter_by(login=login).first()
			session['user_id'] = user.user_id
		return redirect('/')
	return redirect('/')


# Маршрут для выхода из аккаунта
@auth_bp.route('/logout', methods=['POST'])
def logout():
	session.clear()
	return redirect('/')


# Маршрут для отображения страницы профиля
@auth_bp.route('/profile')
def profile():
	user_id = session.get('user_id')
	if user_id:
		with Session as SQLsession:
			user = SQLsession.get(Users, user_id)
			return render_template('profile.html', user=user)

	return redirect('/login')
