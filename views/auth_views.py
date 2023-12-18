from flask import Blueprint, render_template, redirect, flash, request, session, jsonify
from db_manager import get_session
from datetime import datetime
from classes.users import Users
import hash


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
				return redirect('/login')

			user.password_hash = hash.convert_from_db_format(user.password_hash)
			is_password_valid = hash.verify_password(password, user.password_hash)
			print("Is Password Valid:", is_password_valid)
			# Успешный вход, устанавливаем пользователя в сессию
			if is_password_valid:
				session['user_id'] = user.user_id
				flash('Вы успешно вошли в систему!', 'success')
				return redirect('/')

			# Неправильный логин или пароль, выводим сообщение об ошибке
			else:
				flash('Неправильный логин или пароль. Пожалуйста, попробуйте снова.', 'error')
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
@auth_bp.route('/register', methods=['GET', 'POST'])
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
		with Session as SQLsession:
			existing_user = SQLsession.query(Users).filter_by(login=login).first()
			if existing_user:
				return jsonify({'error': 'Пользователь с таким логином уже существует'})

		with Session as SQLsession:
			new_user = Users(login=login, password_hash=db_hash, created_at=datetime.now(), email=email, name=name, surname=surname)
			SQLsession.add(new_user)
			SQLsession.commit()
			user = SQLsession.query(Users).filter_by(login=login).first()
			session['user_id'] = user.user_id
		return redirect('/')

	return render_template('register.html')


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
