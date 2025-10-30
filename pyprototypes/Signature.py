import inspect
from collections.abc import Callable
from dataclasses import dataclass
from inspect import Parameter


@dataclass
class MetaSignature:
	name: str
	func: Callable
	signature: dict[str, type]


class SignatureConstructed:
	@staticmethod
	def signature(template: callable) -> MetaSignature:
		annotations = template.__annotations__
		varnames = template.__code__.co_varnames
		argcount = template.__code__.co_argcount
		posonlycount = template.__code__.co_posonlyargcount
		signature = {
			arg: Parameter.empty if arg not in annotations else annotations[arg]
			for arg in varnames[posonlycount:argcount]
		}
		return MetaSignature(template.__name__, template, signature)


class SignatureInspect:
	"""Collects signature"""

	@staticmethod
	def signature(template: Callable) -> MetaSignature:
		p = inspect.signature(template).parameters.values()
		return MetaSignature(
			template.__name__,
			template,
			{param.name: param.annotation for param in p},
		)
