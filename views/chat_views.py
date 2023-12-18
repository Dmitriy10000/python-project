from flask import Blueprint, session, render_template, redirect
from utils.db_manager import get_session
from classes.users import Users
from classes.friends import Friends
from classes.chats import Chats
from classes.chat_members import ChatMembers


chat_bp = Blueprint('auth', __name__)
Session = get_session()


# Маршрут для чата
@chat_bp.route('/chat', methods=['GET', 'POST'])
def chat():
	user_id = session.get('user_id')
	if user_id:
		with Session as SQLsession:
			user = SQLsession.get(Users, user_id)
			
			# Получаем список друзей
			friends = SQLsession.query(Friends).filter_by(user_id1=user_id).all()
			friends += SQLsession.query(Friends).filter_by(user_id2=user_id).all()
			friends_list = []
			for friend in friends:
				if friend.user_id1 == user_id:
					friends_list.append(SQLsession.query(Users).get(friend.user_id2))
				else:
					friends_list.append(SQLsession.query(Users).get(friend.user_id1))
			print('friends_list', friends_list)

			# Получаем список чатов
			chats = SQLsession.query(ChatMembers).filter_by(user_id=user_id).all()
			chats_list = []
			for chat in chats:
				chats_list.append(SQLsession.query(Chats).get(chat.chat_id))
			print('chats_list', chats_list)
			return render_template('chat.html', user=user, friends_list=friends_list, chats_list=chats_list)
		
	else:
		return redirect('/login')