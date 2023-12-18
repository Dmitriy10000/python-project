from flask import Blueprint, session, render_template, redirect, request, jsonify
from utils.db_manager import get_session
from classes.users import Users
from classes.friends import Friends
from classes.chats import Chats
from classes.chat_members import ChatMembers
from classes.messages import Messages
from datetime import datetime


chat_bp = Blueprint('auth', __name__)
Session = get_session()


# Маршрут для чата
@chat_bp.route('/chat', methods=['GET'])
def chat():
	# Проверяем авторизован ли пользователь
	user_id = session.get('user_id')
	if not user_id:
		return redirect('/login')
	
	# Получаем данные пользователя
	with Session as SQLSession:
		user = SQLSession.query(Users).filter(Users.user_id == user_id).first()

	# Проверяем, выбран ли чат
	chat_id = request.args.get('id')
	if chat_id == None:
		return render_template('chat.html', user=user)
	
	# Проверяем, существует ли чат
	with Session as SQLSession:
		chat = SQLSession.query(Chats).filter(Chats.chat_id == chat_id).first()
	if not chat:
		return redirect('/chat')

	# Проверяем, является ли пользователь участником чата
	with Session as SQLSession:
		chat_member = SQLSession.query(ChatMembers).filter(ChatMembers.chat_id == chat_id).filter(ChatMembers.user_id == user_id).first()
	if not chat_member:
		return redirect('/chat')
	
	# Получаем 20 последних сообщений
	with Session as SQLSession:
		messages = SQLSession.query(Messages).filter(Messages.chat_id == chat_id).order_by(Messages.timestamp.desc()).limit(20).all()
	print('Получили 20 последних сообщений')

	# Получаем участников чата
	with Session as SQLSession:
		chat_members = SQLSession.query(ChatMembers).filter(ChatMembers.chat_id == chat_id).all()
	print('Получили участников чата')

	# Возвращаем страницу чата
	return render_template('chat.html', user=user, chat=chat, messages=messages, chat_members=chat_members)


# # Маршрут для получения сообщений
# @chat_bp.route('/get_messages', methods=['POST', 'GET'])
# def get_messages():
# 	# Проверяем авторизован ли пользователь
# 	user_id = session.get('user_id')
# 	if not user_id:
# 		return redirect('/login')
	
# 	# Получаем данные пользователя
# 	with Session as SQLSession:
# 		user = SQLSession.query(Users).filter(Users.user_id == user_id).first()

# 	# Проверяем, выбран ли чат
# 	chat_id = request.args.get('id')
# 	if chat_id == None:
# 		return render_template('chat.html', user=user)
	
# 	# Проверяем, существует ли чат
# 	with Session as SQLSession:
# 		chat = SQLSession.query(Chats).filter(Chats.chat_id == chat_id).first()
# 	if not chat:
# 		return redirect('/chat')

# 	# Проверяем, является ли пользователь участником чата
# 	with Session as SQLSession:
# 		chat_member = SQLSession.query(ChatMembers).filter(ChatMembers.chat_id == chat_id).filter(ChatMembers.user_id == user_id).first()
# 	if not chat_member:
# 		return redirect('/chat')
	
# 	# Получаем 20 последних сообщений
# 	with Session as SQLSession:
# 		messages = SQLSession.query(Messages).filter(Messages.chat_id == chat_id).order_by(Messages.timestamp.desc()).limit(20).all()
# 	print('Получили 20 последних сообщений')

# 	# Получаем участников чата
# 	with Session as SQLSession:
# 		chat_members = SQLSession.query(ChatMembers).filter(ChatMembers.chat_id == chat_id).all()
# 	print('Получили участников чата')

# 	# Возвращаем страницу чата
# 	# post запрос
# 	# if request.method == 'POST':
# 	# Пакуем данные в json
# 	data = {
# 		'messags': messages,
# 		'chat_members': chat_members
# 	}
# 	# Возвращаем json
# 	print('data', data)
# 	return jsonify(data)


# Маршрут для чата
@chat_bp.route('/personal_messages', methods=['POST'])
def personal_messages():
	# Проверяем авторизован ли пользователь
	user_id = session.get('user_id')
	if not user_id:
		return redirect('/login')
	print('user_id', user_id)

	# Проверяем, существует ли чат, где участником является наш собеседник
	target_id = request.form.get('user_id')
	print('target_id', target_id)
	with Session as SQLSession:
		# Ищем все чаты текущего пользователя
		chats = SQLSession.query(ChatMembers).filter(ChatMembers.user_id == user_id).all()
		# Получаем имя и фамилию собеседника
		target = SQLSession.query(Users).filter(Users.user_id == target_id).first()
		for chat in chats:
			tmp = SQLSession.query(ChatMembers).filter(ChatMembers.chat_id == chat.chat_id).filter(ChatMembers.user_id == target_id).first()
			# Когда нашли чат, где участником является наш собеседник
			if tmp:
				# Получаем 20 последних сообщений
				messages = SQLSession.query(Messages).filter(Messages.chat_id == chat.chat_id).order_by(Messages.timestamp.desc()).limit(20).all()
				# Пакуем данные в json
				data = {
					'messages': messages,
					'chat_id': chat.chat_id,
					'chat_name': target.name + ' ' + target.surname
				}
				# Возвращаем json
				print('data', data)
				return jsonify(data)
	
	# Создаем чат
	with Session as SQLSession:
		chat = Chats()
		chat.chat_name = 'PM'
		chat.type = 'PM'
		chat.created_at = datetime.now()
		SQLSession.add(chat)
		SQLSession.flush()
		chat_member = ChatMembers()
		chat_member.chat_id = chat.chat_id
		chat_member.user_id = user_id
		chat_member.is_admin = True
		chat_member.joined_at = datetime.now()
		SQLSession.add(chat_member)
		chat_member = ChatMembers()
		chat_member.chat_id = chat.chat_id
		chat_member.user_id = target_id
		chat_member.is_admin = True
		chat_member.joined_at = datetime.now()
		SQLSession.add(chat_member)
		SQLSession.commit()

	with Session as SQLSession:
		# Ищем все чаты текущего пользователя
		chats = SQLSession.query(ChatMembers).filter(ChatMembers.user_id == user_id).all()
		# Получаем имя и фамилию собеседника
		target = SQLSession.query(Users).filter(Users.user_id == target_id).first()
		for chat in chats:
			tmp = SQLSession.query(ChatMembers).filter(ChatMembers.chat_id == chat.chat_id).filter(ChatMembers.user_id == target_id).first()
			# Когда нашли чат, где участником является наш собеседник
			if tmp:
				# Получаем 20 последних сообщений
				messages = SQLSession.query(Messages).filter(Messages.chat_id == chat.chat_id).order_by(Messages.timestamp.desc()).limit(20).all()
				# Пакуем данные в json
				data = {
					'user_id': user_id,
					'target_id': target_id,
					'chat_id': chat.chat_id,
					'chat_name': target.name + ' ' + target.surname,
					'messages': messages,
				}
				# Возвращаем json
				print('data', data)
				return jsonify(data)
			
	# Если не нашли чат, то возвращаем ошибку
	return jsonify({'error': 'Чат не найден'})