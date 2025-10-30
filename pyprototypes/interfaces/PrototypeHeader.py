from __future__ import annotations

from abc import abstractmethod
from collections.abc import Callable
from typing import Protocol

import pyprototypes.prototype as prototype
from pyprototypes.interfaces.FixtureMatcherHeader import FixtureMatcher_t
from pyprototypes.interfaces.SignatureMatcherHeader import SignatureMatcher_t


class Prototype_T(Protocol):
	signature_matcher: SignatureMatcher_t
	fixture_matcher: FixtureMatcher_t

	@classmethod
	@abstractmethod
	def typed(cls, prototype: Callable) -> Prototype_T:
		raise NotImplementedError

	@abstractmethod
	def fixture(self, fnc: Callable) -> Callable:
		raise NotImplementedError

	@abstractmethod
	def function(self, fnc: Callable) -> Callable:
		raise NotImplementedError

	@abstractmethod
	def check(self, fnc: Callable) -> prototype.ProtocolCode:
		raise NotImplementedError
