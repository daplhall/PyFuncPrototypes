import inspect
from pyprototypes.BaseMatchers import FuncMetaData


class UnsupportedParameters(Exception):
	def __init__(self, error_msg: str, meta: FuncMetaData):
		super().__init__(
			f"\nError in the signature of '{meta.name}' "
			f"in {meta.loc}\n" + error_msg
		)
