
# Импортирование всех полезных модулей
from .longpolling import LongPoll
from .handler import Handler
from .utils import Utils

# Ядро бота, основанное на использовании готовых модулей
class Core(LongPoll, Handler, Utils):
	def __init__(self):
		LongPoll.__init__(self)
		Handler.__init__(self)

		# Поля, которые должны быть переопределены
		self.config = None # Поле с конфигурацией
		self.api = None # Поле с API-объектом (vk.API)
		self.id = None # Поле с ID сообщества

	def start(self):
		""" Начинает получение событий (использует методы класса LongPoll и Handler) """

		while True:
			try:
				self.listen(self.check)

			except Exception as e:
				if self.config.log_errors:
					print(f"{type(e).__name__}: {e}")

				else:
					raise