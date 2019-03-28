
import requests

class LongPoll:
	"""
		Специальный класс для LongPolling.
	"""
	def __init__(self):
		self._server = None
		self._key = None
		self._ts = None

	def get_longpoll_data_response(self):
		""" Получение событий """
		return requests.get('{self._server}?act=a_check&key={self._key}&ts={self._ts}&wait=25'.format(self = self)).json()

	def get_longpoll_server_response(self):
		""" Получение LongPoll-данных, необходимых для работы """
		return self.api.groups.getLongPollServer(group_id = self.id)

	def in_process(self):
		""" Проверяет, инициализированы ли LongPoll-данные """
		return self._server and self._key and self._ts

	def restart(self):
		""" Перезаписывает LongPoll-данные. Фактически заново начинает работу """
		lps = self.get_longpoll_server_response()
		self._server = lps['server']
		self._key = lps['key']
		self._ts = lps['ts']

	def get_longpoll_data(self):
		""" Основной метод для работы с Long Poll """
		if not self.in_process(): # Если не инициализированы LongPoll-данные
			self.restart() # Перезапуск

		try:
			response = self.get_longpoll_data_response() # Получаем события
			assert 'failed' not in response

		except: # Если возникло исключение при получении данных
			self.restart() # Перезапуск
			return self.get_longpoll_data() # Заново вызывается метод

		self._ts = response.get('ts') # Обновляем номер событий
		return response # Возвращаем список событий

	def listen(self, callback):
		""" Прослушка """
		while True:
			response = self.get_longpoll_data()
			callback(response.get('updates', [])) # Вызов метода, обрабатывающего данные события