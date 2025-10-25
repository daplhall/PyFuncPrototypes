class DictStack:
	def __init__(self, di):
		self._dict = di
		self._iter = iter(di.items())
		self._name, self._type = next(self._iter, (None, None))

	def pop(self):
		name, typ = self._name, self._type
		self._name, self._type = next(self._iter, (None, None))
		return name, typ

	def __contains__(self, value):
		return value in self._dict

	def top(self):
		return self._name, self._type

	def __bool__(self):
		return bool(self._name)
