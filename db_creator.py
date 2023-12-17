from classes.users import Users
from classes.friends import Friends
from classes.invites import Invites
from classes.messages import Messages
from classes.chats import Chats
from classes.chat_members import ChatMembers

def create_database_tables(engine):
	# Создаем таблицы в базе данных
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