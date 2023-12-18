from flask import Blueprint, request, session, jsonify
from db_manager import get_session
from classes.users import Users
from classes.friends import Friends
from classes.invites import Invites


search_bp = Blueprint('auth', __name__)
Session = get_session()



# Принимаем ajax запрос на получение списка друзей и возвращаем json
@search_bp.route('/global_user_search', methods=['POST'])
def global_user_search():
	print(request.form)
	search_query = request.form['search_query']

	# Проверяем запрос на пустоту
	if search_query == '':
		return jsonify({'error': 'Пустой запрос'})
	
	# Ищем пользователей по запросу
	with Session as SQLsession:
		users = SQLsession.query(Users).filter(Users.login.ilike(f"%{search_query}%")).all()

	# Удаляем из списка текущего пользователя
	user_id = session.get('user_id')
	for user in users:
		if user.user_id == user_id:
			users.remove(user)
			break

	# Пакуем данные в json и отправляем
	users_json = []
	with Session as SQLsession:
		for user in users:
			# Проверяем, не являются ли пользователи друзьями
			# user_id1 меньше user_id2
			exiting_friend = SQLsession.query(Friends).filter_by(user_id1=min(user_id, user.user_id), user_id2=max(user_id, user.user_id)).first()
			if exiting_friend:
				users_json.append({'user_id': user.user_id, 'login': user.login, 'name': user.name, 'surname': user.surname, 'is_friend': True})
				continue

			# Проверяем, не было ли отправлено исходящее приглашение
			existing_invite = SQLsession.query(Invites).filter_by(user_id1=user_id, user_id2=user.user_id).first()
			if existing_invite:
				users_json.append({'user_id': user.user_id, 'login': user.login, 'name': user.name, 'surname': user.surname, 'is_invite_sent': True})
				continue

			# Проверяем, не было ли получено входящее приглашение
			existing_invite = SQLsession.query(Invites).filter_by(user_id1=user.user_id, user_id2=user_id).first()
			if existing_invite:
				users_json.append({'user_id': user.user_id, 'login': user.login, 'name': user.name, 'surname': user.surname, 'is_invite_received': True})
				continue

			# Если ничего не найдено, то добавляем пользователя в список
			users_json.append({'user_id': user.user_id, 'login': user.login, 'name': user.name, 'surname': user.surname, 'is_friend': False})
	return jsonify(users_json)