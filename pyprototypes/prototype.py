from typing import Any

from pyprototypes.BaseMatchers import NameMatcher, Signature
from pyprototypes.FixtureMachine import FixtureMachine
from pyprototypes.FunctionMetaData import FuncMeta
from pyprototypes.NameTypeMachine import MatcherMachine


class Prototype:
	def __init__(self, prototype: callable, is_typed=False):
		self.signature = Signature.signature(prototype)
		self.fixtures = {}
		self.is_typed = is_typed

	@classmethod
	def typed(cls, prototype: callable):
		self = cls(prototype)
		self.is_typed = True
		return self

	def fixture(self, fnc) -> callable:
		if NameMatcher.match_str(self.signature, fnc.__name__):
			meta = FuncMeta(fnc)
			self.fixtures[meta.name] = meta
			return fnc
		else:
			raise Exception("Fixture doesn't match name")

	def wrap(self, fnc: callable, applyables: dict[str, Any]) -> callable:
		def wrapper(**kwards):
			kwards.update(applyables)
			return fnc(**kwards)

		return wrapper

	def check(self, fnc: callable) -> callable:
		ntmatcher = MatcherMachine()
		inpt_sig = Signature.signature(fnc)
		meta = Signature.metadata(fnc)
		if not ntmatcher.match(self.signature, inpt_sig, meta, self.is_typed):
			return NotImplemented
		if not self.fixtures:
			return fnc
		else:
			fixt_machine = FixtureMachine()
			kwards = fixt_machine.match(inpt_sig, self.fixtures)
			return self.wrap(fnc, kwards)
