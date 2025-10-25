from pyprototypes.BaseMatchers import Signature


class FuncMeta:
	def __init__(self, function):
		self._name = function.__name__
		self._qualname = function.__qualname__
		self._module = function.__module__
		self._func = function
		self._signature = Signature.signature(function)

	@property
	def name(self):
		return self._name

	@property
	def qualname(self):
		return self._qualname

	@property
	def module(self):
		return self._module

	@property
	def func(self):
		return self._func

	@property
	def signature(self):
		return self._signature
