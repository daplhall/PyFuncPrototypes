from abc import abstractmethod
from collections.abc import Callable
from enum import IntEnum, auto
from typing import Any, Protocol

from pyprototypes.arguments import ArgChecker, ArgChecker_t
from pyprototypes.fixtures import FixFinder, FixFinder_t
from pyprototypes.signature import (
	SigMeta,
	SigFetcher_t,
	SignatureConstructed,
)


class PrototypeCode(IntEnum):
	OK = auto()
	FAIL = auto()


class Prototype_t(Protocol):
	@classmethod
	@abstractmethod
	def typed(cls, prototype: Callable) -> "Prototype_t":
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


class Prototype(Prototype_t):
	def __init__(
		self,
		prototype: Callable,
		*,
		fix_finder: FixFinder_t = FixFinder(),
		arg_checker: ArgChecker_t = ArgChecker(typed=False),
		sig_fetcher: SigFetcher_t = SignatureConstructed,
	):
		self._fix_finder = fix_finder
		self._arg_checker = arg_checker
		self._sig_fetcher = sig_fetcher

		self._reference = self._signature(prototype)
		self._fixtures: dict[str, SigMeta] = {}

	@classmethod
	def typed(
		cls,
		prototype: Callable,
		*,
		arg_checker=ArgChecker(typed=True),
	) -> Prototype_t:
		return cls(
			prototype,
			arg_checker=arg_checker,
		)

	def _wrap(self, fnc: Callable, defaults: dict[str, Any]) -> Callable:
		def wrapper(**kwards):
			kwards.update(defaults)
			return fnc(**kwards)

		return wrapper

	def _signature(self, fnc: Callable) -> SigMeta:
		return self._sig_fetcher.fetch(fnc)

	def fixture(self, fnc) -> Callable:
		meta = self._signature(fnc)
		self._fixtures[meta.name] = meta
		return fnc

	def function(self, fnc: Callable) -> Callable:
		fnc_sig = self._signature(fnc)
		self._arg_checker.match(self._reference, fnc_sig)
		if self._fixtures:
			kwargs = self._fix_finder.match(fnc_sig, self._fixtures)
			fnc = self._wrap(fnc, kwargs)
		setattr(fnc, f"{self}_tag", True)
		return fnc

	def check(self, fnc: Callable) -> PrototypeCode:
		if hasattr(fnc, f"{self}_tag"):
			return PrototypeCode.OK
		else:
			return PrototypeCode.FAIL
