from abc import abstractmethod
from typing import Protocol

from pyprototypes.Signature import MetaSignature


class SignatureMatcher_t(Protocol):
	is_typed: bool

	@abstractmethod
	def match(self, reference: MetaSignature, signature: MetaSignature) -> bool:
		raise NotImplementedError
