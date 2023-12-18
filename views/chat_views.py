from flask import Blueprint, session, render_template, redirect, request
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
@chat_bp.route('/chat', methods=['GET', 'POST'])
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
	
	# Проверяем, существует ли чат, где участником является пользователь
	with Session as SQLSession:
		chat = SQLSession.query(Chats).join(ChatMembers).filter(ChatMembers.user_id == user_id).filter(Chats.chat_id == chat_id).first()
		print(chat)
		if not chat:
			return redirect('/chat')
		
		# Получаем последние 20 сообщений
		messages = SQLSession.query(Messages).filter(Messages.chat_id == chat_id).order_by(Messages.message_id.desc()).limit(20).all()
		messages.reverse()

		return render_template('chat.html', user=user, chat=chat, messages=messages)





# Маршрут для создания чата
@chat_bp.route('/create_chat', methods=['POST'])
def create_chat():
	# Проверяем авторизован ли пользователь
	user_id = session.get('user_id')
	if not user_id:
		return redirect('/login')
	print('user_id', user_id)

	# Проверяем, существует ли чат, где участником является пользователь
	target_id = request.form.get('user_id')
	print('target_id', target_id)
	with Session as SQLSession:
		# Проверяем, существует ли чат, где участником является пользователь
		chat = (
			SQLSession.query(Chats)
			.join(ChatMembers, Chats.chat_id == ChatMembers.chat_id)
			.filter(ChatMembers.user_id == user_id)
			.filter(ChatMembers.user_id == target_id)
			.first()
		)
		print('chat', chat)
		if chat:
			return redirect('/chat?id=' + str(chat.chat_id))
	
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
		
	print('CHAT ID:', str(chat.chat_id))
	return redirect('/chat?id=' + str(chat.chat_id))