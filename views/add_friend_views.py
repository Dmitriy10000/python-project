from flask import Blueprint, redirect, request, session, jsonify
from utils.db_manager import get_session
from classes.users import Users
from classes.friends import Friends
from classes.invites import Invites


add_friend_bp = Blueprint('auth', __name__)
Session = get_session()


# Создаем маршрут для добавления друзей
@add_friend_bp.route('/add_friend', methods=['POST'])
def add_friend():
	print(request.form)
	user_id1 = session.get('user_id')
	user_id2 = request.form['user_id']
	request_type = request.form['request_type']

	# Если пользователь не авторизован, то перенаправляем на страницу входа
	if not user_id1:
		return redirect('/login')

	with Session as SQLsession:
		# Проверяем, существует ли пользователь с таким id
		existing_user = SQLsession.query(Users).filter_by(user_id=user_id1).first()
		if not existing_user:
			print('Пользователь 1 не найден')
			return jsonify({'error': 'Пользователь 1 не найден'})

		# Проверяем, существует ли пользователь с таким id
		existing_user = SQLsession.query(Users).filter_by(user_id=user_id2).first()
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
			# user_id1 меньше user_id2
			existing_friend = SQLsession.query(Friends).filter_by(user_id1=min(int(user_id1), int(user_id2)), user_id2=max(int(user_id1), int(user_id2))).first()
			if existing_friend:
				print('Пользователь уже является другом')
				return jsonify({'error': 'Пользователь уже является другом'})
			
			# Проверяем, не было ли уже отправлено приглашение
			existing_invite = SQLsession.query(Invites).filter_by(user_id1=user_id1, user_id2=user_id2).first()
			if existing_invite:
				print('Приглашение уже отправлено')
				return jsonify({'error': 'Приглашение уже отправлено'})
			
			# Проверяем, не было ли уже получено приглашение
			existing_invite = SQLsession.query(Invites).filter_by(user_id1=user_id2, user_id2=user_id1).first()
			if existing_invite:
				# Добавляем в друзья user_id1 меньше user_id2
				print('Приглашение уже получено, добавляем в друзья')
				new_friend = Friends(user_id1=min(int(user_id1), int(user_id2)), user_id2=max(int(user_id1), int(user_id2)))
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
			SQLsession.add(new_invite)
			SQLsession.commit()
			print('Приглашение успешно отправлено')
			return jsonify({'success': 'Приглашение успешно отправлено'})
		
		# Удаление из друзей
		elif request_type == 'delete':
			print('Удаление из друзей', user_id1, 'к', user_id2)
			# Проверяем, является ли пользователь другом
			# user_id1 меньше user_id2
			existing_friend = SQLsession.query(Friends).filter_by(user_id1=min(int(user_id1), int(user_id2)), user_id2=max(int(user_id1), int(user_id2))).first()
			if not existing_friend:
				print('Пользователь не является другом')
				return jsonify({'error': 'Пользователь не является другом'})
			
			# Удаляем из друзей
			SQLsession.query(Friends).filter_by(user_id1=min(int(user_id1), int(user_id2)), user_id2=max(int(user_id1), int(user_id2))).delete()
			SQLsession.commit()
			print('Пользователь успешно удален из друзей')
			return jsonify({'success': 'Пользователь успешно удален из друзей'})
		
		# Отмена приглашения
		elif request_type == 'cancel':
			print('Отмена приглашения', user_id1, 'к', user_id2)

			# Проверяем, было ли отправлено приглашение
			existing_invite = SQLsession.query(Invites).filter_by(user_id1=user_id1, user_id2=user_id2).first()
			if not existing_invite:
				print('Приглашение не было отправлено')
				return jsonify({'error': 'Приглашение не было отправлено'})
			
			# Удаляем приглашение
			SQLsession.query(Invites).filter_by(user_id1=user_id1, user_id2=user_id2).delete()
			SQLsession.commit()
			print('Приглашение успешно отменено')
			return jsonify({'success': 'Приглашение успешно отменено'})
		
		# Отклонение приглашения
		elif request_type == 'decline':
			print('Отклонение приглашения', user_id1, 'к', user_id2)
			# Проверяем, было ли получено приглашение
			existing_invite = SQLsession.query(Invites).filter_by(user_id1=user_id2, user_id2=user_id1).first()
			if not existing_invite:
				print('Приглашение не было получено')
				return jsonify({'error': 'Приглашение не было получено'})
			
			# Удаляем приглашение
			SQLsession.query(Invites).filter_by(user_id1=user_id2, user_id2=user_id1).delete()
			SQLsession.commit()
			print('Приглашение успешно отклонено')
			return jsonify({'success': 'Приглашение успешно отклонено'})
		
		# Принятие приглашения
		elif request_type == 'accept':
			print('Принятие приглашения', user_id1, 'к', user_id2)
			# Проверяем, было ли получено приглашение
			existing_invite = SQLsession.query(Invites).filter_by(user_id1=user_id2, user_id2=user_id1).first()
			if not existing_invite:
				print('Приглашение не было получено')
				return jsonify({'error': 'Приглашение не было получено'})
			
			# Проверяем, не является ли пользователь другом
			# user_id1 меньше user_id2
			existing_friend = SQLsession.query(Friends).filter_by(user_id1=min(int(user_id1), int(user_id2)), user_id2=max(int(user_id1), int(user_id2))).first()
			if existing_friend:
				print('Пользователь уже является другом')
				return jsonify({'error': 'Пользователь уже является другом'})
			
			# Добавляем в друзья
			# user_id1 меньше user_id2
			new_friend = Friends(user_id1=min(int(user_id1), int(user_id2)), user_id2=max(int(user_id1), int(user_id2)))
			SQLsession.add(new_friend)
			SQLsession.commit()
			print('Пользователь успешно добавлен в друзья')

			# Удаляем приглашение
			SQLsession.query(Invites).filter_by(user_id1=user_id2, user_id2=user_id1).delete()
			SQLsession.commit()
			print('Приглашение удалено')
			return jsonify({'success': 'Пользователь успешно добавлен в друзья'})
