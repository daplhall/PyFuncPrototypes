import inspect
from abc import abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from inspect import Parameter
from typing import Protocol

from pyprototypes._typing import Signature


@dataclass
class SigMeta:
	name: str
	func: Callable
	signature: Signature


class SigFetcher_t(Protocol):
	@staticmethod
	@abstractmethod
	def fetch(template: Callable) -> SigMeta:
		raise NotImplementedError


class SignatureConstructed(SigFetcher_t):
	@staticmethod
	def fetch(template: Callable) -> SigMeta:
		annotations = template.__annotations__
		varnames = template.__code__.co_varnames
		argcount = template.__code__.co_argcount
		posonlycount = template.__code__.co_posonlyargcount
		signature = {
			arg: Parameter.empty if arg not in annotations else annotations[arg]
			for arg in varnames[posonlycount:argcount]
		}
		return SigMeta(template.__name__, template, signature)


class SignatureInspect(SigFetcher_t):
	"""Collects signature"""

	@staticmethod
	def fetch(template: Callable) -> SigMeta:
		p = inspect.signature(template).parameters.values()
		return SigMeta(
			template.__name__,
			template,
			{param.name: param.annotation for param in p},
		)
