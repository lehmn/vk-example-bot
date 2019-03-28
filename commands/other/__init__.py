
from ..command import Request

class Hello(Request):
	def call(self):
		self.response(message = f"Привет! Твои аргументы: { self.bot.filter(' '.join(self.args)) }")