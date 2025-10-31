from abc import abstractmethod
from collections.abc import Callable
from enum import IntEnum, auto
from typing import Any, Protocol

from pyprototypes.fixturemachine import FixtureMachine, FixtureMatcher_t
from pyprototypes.signature import (
	MetaSignature,
	Signature_T,
	SignatureConstructed,
)
from pyprototypes.signaturemachine import SignatureMachine, SignatureMatcher_t

TYPED = True


class PrototypeCode(IntEnum):
	OK = auto()
	FAIL = auto()


class Prototype_T(Protocol):
	@classmethod
	@abstractmethod
	def typed(cls, prototype: Callable) -> "Prototype_T":
		raise NotImplementedError

	@abstractmethod
	def fixture(self, fnc: Callable) -> Callable:
		raise NotImplementedError

	@abstractmethod
	def function(self, fnc: Callable) -> Callable:
		raise NotImplementedError

	@abstractmethod
	def check(self, fnc: Callable) -> PrototypeCode:
		raise NotImplementedError


class Prototype:
	def __init__(
		self,
		prototype: Callable,
		*,
		fixture_matcher: FixtureMatcher_t = FixtureMachine(),
		signature_matcher: SignatureMatcher_t = SignatureMachine(not TYPED),
		signature_pipeline: Signature_T = SignatureConstructed,
	):
		self.signature_matcher = signature_matcher
		self.fixture_matcher = fixture_matcher
		self._get_signature = signature_pipeline

		self._signature = signature_pipeline.signature(prototype)
		self._fixtures: dict[str, MetaSignature] = {}

	@classmethod
	def typed(
		cls,
		prototype: Callable,
		*,
		fixture_matcher=FixtureMachine(),
		signature_matcher=SignatureMachine(TYPED),
		signature_pipeline=SignatureConstructed,
	) -> Prototype_T:
		self = cls(
			prototype,
			fixture_matcher=fixture_matcher,
			signature_matcher=signature_matcher,
			signature_pipeline=signature_pipeline,
		)
		return self

	def fixture(self, fnc) -> Callable:
		meta = self._get_signature.signature(fnc)
		self._fixtures[meta.name] = meta
		return fnc

	def _wrap(self, fnc: Callable, defaults: dict[str, Any]) -> Callable:
		def wrapper(**kwards):
			kwards.update(defaults)
			return fnc(**kwards)

		return wrapper

	def function(self, fnc: Callable) -> Callable:
		inpt_sig = self._get_signature.signature(fnc)
		self.signature_matcher.match(self._signature, inpt_sig)
		if self._fixtures:
			kwargs = self.fixture_matcher.match(inpt_sig, self._fixtures)
			fnc = self._wrap(fnc, kwargs)
		setattr(fnc, f"{self}_tag", True)
		return fnc

	def check(self, fnc: Callable) -> PrototypeCode:
		if hasattr(fnc, f"{self}_tag"):
			return PrototypeCode.OK
		else:
			return PrototypeCode.FAIL
