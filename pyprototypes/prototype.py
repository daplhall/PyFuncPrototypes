from collections.abc import Callable
from typing import Any

from pyprototypes.BaseMatchers import NameMatcher, Signature
from pyprototypes.FixtureMachine import FixtureMachine
from pyprototypes.FunctionMetaData import FuncMeta
from pyprototypes.NameTypeMachine import MatcherMachine


class Prototype:
	def __init__(self, prototype: Callable, is_typed=False):
		self.signature = Signature.signature(prototype)
		self.fixtures: dict[str, FuncMeta] = {}
		self.is_typed = is_typed

	@classmethod
	def typed(cls, prototype: Callable):
		self = cls(prototype)
		self.is_typed = True
		return self

	def fixture(self, fnc) -> Callable:
		meta = FuncMeta(fnc)
		self.fixtures[meta.name] = meta
		return fnc

	def wrap(self, fnc: Callable, defaults: dict[str, Any]) -> Callable:
		def wrapper(**kwards):
			kwards.update(defaults)
			return fnc(**kwards)

		return wrapper

	def check(self, fnc: Callable) -> Callable:
		matcher = MatcherMachine()
		inpt_sig = Signature.signature(fnc)
		meta = Signature.metadata(fnc)
		matcher.match(self.signature, inpt_sig, meta, self.is_typed)
		if self.fixtures:
			fixturematcher = FixtureMachine()
			kwards = fixturematcher.match(inpt_sig, self.fixtures)
			return self.wrap(fnc, kwards)
		else:
			return fnc
