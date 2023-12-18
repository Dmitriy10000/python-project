from flask import Blueprint, render_template, session
from utils.db_manager import get_session
from classes.users import Users


index_bp = Blueprint('auth', __name__)
Session = get_session()


# Функция для получения текущего пользователя из сессии, которая возвращает текущего пользователя или None
def get_logged_in_user():
	user_id = session.get('user_id')
	if user_id:
		with Session as SQLsession:
			temp = SQLsession.get(Users, user_id)
			return temp
	
	return None


# Маршрут для отображения домашней страницы
@index_bp.route('/')
def home():
	user = get_logged_in_user()
	return render_template('login.html', user=user)