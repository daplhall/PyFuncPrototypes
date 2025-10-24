class Prototype:
	def __init__(self, fnc: callable):
		return NotImplemented

	def fixture(self, **kwards) -> callable:
		return NotImplemented

	def check(self, fnc: callable) -> bool:
		pass
