from pyprototypes.BaseMatchers import NameMatcher, Signature
from pyprototypes.FunctionMetaData import FuncMeta


class Prototype:
	def __init__(self, prototype: callable):
		self.signature = Signature.signature(prototype)
		self.fixtures = {}

	def fixture(self, fnc) -> callable:
		if NameMatcher.match_str(self.signature, fnc.__name__):
			meta = FuncMeta(fnc)
			self.fixtures[meta.name] = meta
			return fnc
		else:
			raise Exception("Fixture doesn't match name")

	def machine(self):
		return {name: meta.func for name, meta in self.fixtures.items()}

	def wrap(self, fnc: callable) -> bool:
		def wrapper(**kwards):
			applyed_fixtures = {
				name: func() for name, func in self.machine().items()
			}
			kwards.update(applyed_fixtures)
			return fnc(**kwards)

		return wrapper
