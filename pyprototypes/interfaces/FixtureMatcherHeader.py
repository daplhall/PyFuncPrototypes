from abc import abstractmethod
from typing import Any, Protocol

from pyprototypes.BaseMatchers import MetaSignature


class FixtureMatcher_t(Protocol):
	@abstractmethod
	def match(
		self, signature: MetaSignature, fixtures: dict[str, MetaSignature]
	) -> dict[str, Any]:
		raise NotImplementedError
