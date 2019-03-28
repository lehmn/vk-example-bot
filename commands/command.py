
import re

class CommandException(Exception):
	pass

class Request:
	def __init__(self, bot, command, message):
		self.bot = bot # Объект бота
		self.command = command # Введенная команда
		self.message = message # Объект сообщения

		self.peer_id = self.message.get('peer_id')

		self.get_chat_id() # Сразу получаем ID чата.
		self.parse_args() # Сразу начинается парсинг аргументов.

	def get_chat_id(self):
		low_peer_id = self.peer_id - 2000000000
		self.chat_id = low_peer_id if low_peer_id > 0 else 0

		return self.chat_id

	def parse_args(self):
		text = re.sub('^' + self.command.pattern, '', self.message.get('text'))
		self.args = [ i for i in text.split(' ') if i != '' ]

		return self.args

	def call(self):
		pass # Метод, вызываемый при вводе команды. 

	def response(self, **kwargs):
		return self.bot.api.messages.send(
			random_id = 0,
			peer_id = self.peer_id,
			**kwargs
		)

class Command: # Класс команды

	commands = []

	def __init__(self, pattern, name, handler, type = 'all'):
		self.pattern = pattern # Шаблон команды
		self.name = name # Имя команды
		self.handler = handler # Класс, чей метод call вызывается при вводе команды (обработчик)

		self.type = type # Тип диалога, в котором можно вызывать данную команду ('chat', 'pm', 'all')

	def start(self, bot, message): # Запуск обработчика команды
		request = self.handler(bot = bot, command = self, message = message)

		if request.chat_id and self.type == 'pm':
			return request.bot.config.only_pm

		elif not request.chat_id and self.type == 'chat':
			return request.bot.config.only_chat

		if request.bot.config.log_commands:
			log = {
				'command': request.command,
				'args': request.args,
				'from_id': request.message.get('from_id'),
				'chat_id': request.chat_id
			}

			print(log)

		return request.call() # Вызов метода call, который должен быть переопределен (и возврат его результата)

	def __repr__(self):
		return self.pattern

	@classmethod
	def parse(cls, text):
		for command in cls.commands:
			if re.match(command.pattern, text.lower()):
				return command

	@classmethod
	def get(cls, name):
		for command in cls.commands:
			if command.name == name:
				return command

def new_command(**kwargs): # Специальная функция для создания новой команды. Следует использовать именно её.

	if Command.get(kwargs.get('name')):
		raise CommandException('Command with this name already is.')

	Command.commands.append(Command(**kwargs))