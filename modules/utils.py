
import time
import json

class Utils:
	"""
		Класс с полезными методами
	"""
	def send_msg(self, **kwargs):
		return self.api.messages.send(random_id = 0, **kwargs)

	def get_chat_users(self, chat_id):
		return self.api.messages.getConversationMembers(peer_id = chat_id + 2000000000)

	def get_chat(self, chat_id):
		return self.api.messages.getConversationsById(peer_ids = chat_id + 2000000000)['items'][0]

	def is_in_chat(self, chat_id, user_id):
		return user_id in [ i['member_id'] for i in self.get_chat_users(chat_id)['items'] ]

	def filter(self, string):
		""" Возвращает отфильтрованную строку, удаляя символы, перечисленные в config.py -> spam """
		leave_loop = 0
		while True:
			for symbol in self.config.spam:
				string = string.replace(symbol, "")

			for symbol in self.config.spam:
				if symbol not in string:
					leave_loop += 1

			if leave_loop >= len(self.config.spam):
				break

		return string

	def get_time(self):
		return int(time.time())

	def is_chat(self, message):
		return message['peer_id'] > 2000000000

	def generate_keyboard(self, one_time = True, buttons = []):
		return json.dumps(
			{
				'one_time': one_time,
				'buttons': buttons
			},
			ensure_ascii = False
		)

	def generate_button(self, label, colour, payload = {}):
		return {
			'action': {
				'type': 'text',
				'payload': json.dumps(payload, ensure_ascii = False),
				'label': label
			},
			'color': colour
		}

	def get_full_name_by_id(self, user_id):
		user = self.api.users.get(user_id = user_id)[0]

		return self.get_full_name(user)

	def get_full_name(self, obj):
		return f"{obj['first_name']} {obj['last_name']}"

	def get_user_by_string(self, chat_id, string):
		members = self.get_chat_users(chat_id)['profiles']

		for user in members:
			full_name = user['first_name'].lower() + " " + user['last_name'].lower()
			
			if string.lower() in [ full_name, ' '.join(full_name.split(' ')[::-1]) ]:
				return user

		for user in members:
			for name in string.lower().split(' '):
				if name in [ user['first_name'].lower(), user['last_name'].lower(), str(user['id']) ]:
					return user