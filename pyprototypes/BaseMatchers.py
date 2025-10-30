from typing import Any


class NameMatcher:
	"""
	needs to contain options
	Idea:
	https://stackoverflow.com/questions/5859561/getting-the-closest-string-match
	"""

	@staticmethod
	def match_str(correct: dict[str, Any], arg: str) -> list[str]:
		""" """
		tmp = []
		for option in correct:
			tmp.append((NameMatcher.lev(option, arg), option))
		tmp.sort()
		return [i[1] for i in tmp if min(tmp)[0] == i[0]]

	@staticmethod
	def has_oddities(correct: dict[str, Any], names: dict[str, Any]) -> bool:
		if set(correct) ^ set(names):
			return True
		else:
			return False

	@staticmethod
	def is_odd(correct: dict[str, Any], name: str) -> bool:
		if not (set(correct) & {name}):
			return True
		else:
			return False

	@staticmethod
	def lev(a: str, b: str) -> int:
		"""
		levenshtein_distance
		https://en.wikipedia.org/wiki/Levenshtein_distance
		"""
		if len(b) == 0:
			return len(a)
		elif len(a) == 0:
			return len(b)
		elif a[0] == b[0]:
			return NameMatcher.lev(a[1:], b[1:])
		else:
			return 1 + min(
				NameMatcher.lev(a[1:], b),
				NameMatcher.lev(a, b[1:]),
				NameMatcher.lev(a[1:], b[1:]),
			)


class TypeMatcher:
	@staticmethod
	def match(
		overlap: set[str],
		reference: dict[Any, type],
		signature: dict[Any, type],
	) -> list[tuple[Any, type, type]]:
		return [
			(param, mytype, reference[param])
			for param, mytype in filter(
				lambda x: x[0] in overlap, signature.items()
			)
			if mytype != reference[param]
		]

	@staticmethod
	def has_oddities(signature: dict[Any, type], inpt: dict[Any, type]):
		if set(signature.items()) - set(inpt.items()):
			return True
		else:
			return False
