
import vk
import config

from modules.core import Core

from commands import * # Инициализация всех команд и импорт класса Command

class Bot(Core):
	""" Класс, в котором стоит творить всю магию """

	def __init__(self):
		super().__init__()

		self.config = config # Вся конфигурация
		self.api = vk.API(vk.Session(config.token), v = config.version) # API объект
		self.id = self.api.groups.getById()[0]['id'] # ID группы

	async def check_message(self, message):
		""" Переопределенный метод, в котором просто ловятся команды. """
		result = None

		command = Command.parse(text = message['text'])
		if command:
			result = command.start(bot = self, message = message)
		
		if result:
			self.send_msg(peer_id = message['peer_id'], message = result)