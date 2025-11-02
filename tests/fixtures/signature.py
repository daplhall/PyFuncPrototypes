import pytest


@pytest.fixture
def kwargs_only():
	def f(bar: int, foo: str):
		pass

	return f


@pytest.fixture
def with_positional():
	def f(bar: int, /, foo: str):
		pass

	return f
