from flask import Blueprint, session, render_template, redirect, request
from utils.db_manager import get_session
from classes.users import Users
from classes.friends import Friends
from classes.chats import Chats
from classes.chat_members import ChatMembers
from classes.messages import Messages


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
		# Получаем список чатов пользователя
		chats = SQLSession.query(ChatMembers).filter(ChatMembers.user_id == user_id).all()

		# Получаем список друзей пользователя
		friends1 = SQLSession.query(Friends).filter(Friends.user_id1 == user_id).all()
		friends2 = SQLSession.query(Friends).filter(Friends.user_id2 == user_id).all()
		friends = []
		for friend in friends1:
			friends.append(SQLSession.query(Users).filter(Users.user_id == friend.user_id2).first())
		for friend in friends2:
			friends.append(SQLSession.query(Users).filter(Users.user_id == friend.user_id1).first())

		# Если пользователь заходит по ссылке, то проверяем, является ли он участником чата
		chat_id = request.args.get('id')
		print('chat_id', chat_id)
		if chat_id != None:
			chat_members = SQLSession.query(ChatMembers).filter(ChatMembers.chat_id == chat_id).all()
			chat_members_user_ids = [chat_member.user_id for chat_member in chat_members]
			if user_id not in chat_members_user_ids:
				return redirect('/chat')
		
		# Получаем последние 20 сообщений
		messages = SQLSession.query(Messages).filter(Messages.chat_id == chat_id).order_by(Messages.message_id.desc()).limit(20).all()
	return render_template('chat.html', chats=chats, friends=friends, messages=messages)


# Маршрут для создания чата
@chat_bp.route('/create_chat', methods=['GET', 'POST'])
def create_chat():
	# Проверяем авторизован ли пользователь
	user_id = session.get('user_id')
	if not user_id:
		return redirect('/login')

	# Проверяем, существует ли чат
	chat_id = request.form.get('chat_id')
	if chat_id:
		with Session as SQLSession:
			chat = SQLSession.query(Chats).filter(Chats.chat_id == chat_id).first()
			if chat:
				return redirect('/chat?id=' + str(chat_id))
	
	# Создаем чат
	with Session as SQLSession:
		chat = Chats()
		SQLSession.add(chat)
		SQLSession.commit()
		chat_id = chat.chat_id