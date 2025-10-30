from abc import abstractmethod
from collections.abc import Callable
from typing import Any, Protocol

from pyprototypes.BaseMatchers import Signature
from pyprototypes.FixtureMachine import FixtureMachine
from pyprototypes.SignatureMachine import SignatureMachine


class Prototype_T(Protocol):
	@classmethod
	@abstractmethod
	def typed(cls, prototype: Callable):
		raise NotImplementedError

	@abstractmethod
	def fixture(self, fnc: Callable) -> Callable:
		raise NotImplementedError

	@abstractmethod
	def function(self, fnc: Callable) -> Callable:
		raise NotImplementedError

	@abstractmethod
	def check(self, fnc: Callable) -> Callable:
		raise NotImplementedError


class Prototype:
	def __init__(self, prototype: Callable, is_typed=False):
		self._signature = Signature.signature(prototype)
		self._fixtures: dict[str,] = {}
		self._is_typed = is_typed

	@classmethod
	def typed(cls, prototype: Callable):
		self = cls(prototype)
		self._is_typed = True
		return self

	def fixture(self, fnc) -> Callable:
		meta = Signature.signature(fnc)
		self._fixtures[meta.name] = meta
		return fnc

	def _wrap(self, fnc: Callable, defaults: dict[str, Any]) -> Callable:
		def wrapper(**kwards):
			kwards.update(defaults)
			return fnc(**kwards)

		return wrapper

	def function(self, fnc: Callable) -> Callable:
		matcher = SignatureMachine(self._is_typed)
		inpt_sig = Signature.signature(fnc)
		matcher.match(self._signature, inpt_sig)
		if self._fixtures:
			fixturematcher = FixtureMachine()
			kwargs = fixturematcher.match(inpt_sig, self._fixtures)
			fnc = self._wrap(fnc, kwargs)
		setattr(fnc, f"{self}_tag", True)
		return fnc

	def check(self, fnc: Callable) -> Callable:
		if out := hasattr(fnc, f"{self}_tag"):
			return out
		else:
			return NotImplemented
