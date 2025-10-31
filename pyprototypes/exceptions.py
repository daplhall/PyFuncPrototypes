import inspect

from pyprototypes.signature import MetaSignature


class UnsupportedParameters(Exception):
	def __init__(self, error_msg: str, meta: MetaSignature):
		super().__init__(
			f"\nError in the signature of '{meta.name}' "
			f"in {inspect.getsourcefile(meta.func)}\n" + error_msg
		)


class FixtureNotDefined(Exception):
	pass


class FixtureRecursionFailed(Exception):
	pass
