from pyprototypes.BaseMatchers import NameMatcher, Signature
from pyprototypes.NameTypeMachine import MatcherMachine


class FuncMeta:
	def __init__(self, function):
		self._name = function.__name__
		self._qualname = function.__qualname__
		self._module = function.__module__
		self._func = function
		self._signature = Signature.signature(function)

	@property
	def name(self):
		return self._name

	@property
	def qualname(self):
		return self._qualname

	@property
	def module(self):
		return self._module

	@property
	def func(self):
		return self._func

	@property
	def Signature(self):
		return self._signature


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

	def check(self, fnc: callable) -> bool:
		return NotImplemented
