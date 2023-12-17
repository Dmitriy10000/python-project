from classes.users import Base as UsersBase, Users
from classes.friends import Base as FriendsBase, Friends
from classes.invites import Base as InvitesBase, Invites
from classes.messages import Base as MessagesBase, Messages
from classes.chats import Base as ChatsBase, Chats
from classes.chat_members import Base as ChatMembersBase, ChatMembers

def create_database_tables(engine):
	UsersBase.metadata.create_all(engine)
	FriendsBase.metadata.create_all(engine)
	InvitesBase.metadata.create_all(engine)
	MessagesBase.metadata.create_all(engine)
	ChatsBase.metadata.create_all(engine)
	ChatMembersBase.metadata.create_all(engine)
	print('Tables created')