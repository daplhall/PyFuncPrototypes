class DictStack:
	def __init__(self, di):
		self._iter = iter(di.signature.items())
		self._name, self._sig = next(self._iter, (None, None))

	def pop(self):
		name, sig = self._name, self._sig
		self._name, self._sig = next(self._iter, (None, None))
		return name, sig

	def top(self):
		return self._name, self._sig

	def __bool__(self):
		return self._name is not None
