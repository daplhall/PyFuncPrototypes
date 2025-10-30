from abc import abstractmethod
from collections.abc import Callable
from typing import Any, Protocol

from pyprototypes.BaseMatchers import Signature, MetaSignature
from pyprototypes.FixtureMachine import FixtureMachine, FixtureMatcher_t
from pyprototypes.SignatureMachine import SignatureMachine, SignatureMatcher_t


class Prototype_T(Protocol):
	signature_matcher: SignatureMatcher_t
	fixture_matcher: FixtureMatcher_t

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
	def __init__(
		self,
		prototype: Callable,
		fixture_matcher: FixtureMatcher_t = FixtureMachine(),
		signature_matcher: FixtureMatcher_t = SignatureMachine(False),
	):
		self.signature_matcher = signature_matcher
		self.fixture_matcher = fixture_matcher

		self._signature = Signature.signature(prototype)
		self._fixtures: dict[str, MetaSignature] = {}

	@classmethod
	def typed(
		cls,
		prototype: Callable,
		fixture_matcher=FixtureMachine(),
		signature_matcher=SignatureMachine(True),
	):
		self = cls(prototype, fixture_matcher, signature_matcher)
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
		inpt_sig = Signature.signature(fnc)
		self.signature_matcher.match(self._signature, inpt_sig)
		if self._fixtures:
			kwargs = self.fixture_matcher.match(inpt_sig, self._fixtures)
			fnc = self._wrap(fnc, kwargs)
		setattr(fnc, f"{self}_tag", True)
		return fnc

	def check(self, fnc: Callable) -> Callable:
		if out := hasattr(fnc, f"{self}_tag"):
			return out
		else:
			return NotImplemented
