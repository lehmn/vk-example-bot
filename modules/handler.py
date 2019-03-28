
import asyncio

class Handler:
	"""
		Специальный класс, ответственный за обработку событий
	"""
	def __init__(self):
		self._events = []
		self._messages = []

		self._event_loop = asyncio.get_event_loop()

	def run_until_complete(self, run_type):
		method = None
		collection = None

		if run_type == 'events':
			method = self.check_event
			collection = self._events

		elif run_type == 'messages':
			method = self.check_message
			collection = self._messages

		else:
			return 'wtf?'

		self._event_loop.run_until_complete(
			asyncio.gather(*[ asyncio.ensure_future(method(i)) for i in collection ])
		)

	def append_message(self, message):
		self._messages.append(message)

	def append_event(self, event):
		self._events.append(event)

	async def check_message(self, message):
		pass

	async def check_event(self, event):
		pass

	def check_events(self):
		self.run_until_complete('events')

		self._events = []

	def check_messages(self):
		self.run_until_complete('messages')

		self._messages = []

	def check(self, updates):
		"""
			Специальный метод, перебирающий все события.

			Для изменения поведения бота нужно переопределить методы:
				self.check_message(self, message) для обработки 1 сообщения;
				self.check_event(self, event) для обработки 1 события;
		"""

		for element in updates: # Перебираем каждое событие
			if element['type'] == 'message_new': # Проверяем, действительно ли нам пришло сообщение
				message = element['object']
					
				if 'action' in message:
					self.append_event(message) # Добавляем в очередь сообщение-событие

				else:
					self.append_message(message) # Добавляем в очередь обычное сообщение

		self.check_events() # Запускаем обработчик сообщений-событий (приглашения, исключения и т.д.)
		self.check_messages() # Запускаем обработчик сообщений