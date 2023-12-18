from classes.users import Base as UsersBase, Users
from classes.friends import Base as FriendsBase, Friends
from classes.invites import Base as InvitesBase, Invites
from classes.messages import Base as MessagesBase, Messages
from classes.chats import Base as ChatsBase, Chats
from classes.chat_members import Base as ChatMembersBase, ChatMembers
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
import json


# Настройки базы данных
with open('DB_cfg.json', 'r') as f:
	DB_cfg = json.load(f)
engine = create_engine(f"postgresql://{DB_cfg['USER']}:{DB_cfg['PASSWORD']}@{DB_cfg['HOST']}:{DB_cfg['PORT']}/{DB_cfg['DB']}")
f.close()
Session = sessionmaker(bind=engine)


def get_session():
	return Session()


def create_database_tables():
	UsersBase.metadata.create_all(engine)
	FriendsBase.metadata.create_all(engine)
	InvitesBase.metadata.create_all(engine)
	MessagesBase.metadata.create_all(engine)
	ChatsBase.metadata.create_all(engine)
	ChatMembersBase.metadata.create_all(engine)
	print('Tables created')