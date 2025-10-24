import pytest


@pytest.fixture
def abc_prototype():
	def SomePrototype(a, b, c):
		pass

	return SomePrototype


@pytest.fixture
def abp_inpt():
	def UserInpt(a, b, p):
		pass

	return UserInpt


@pytest.fixture
def typed_prototype():
	def SomeTypedPrototype(a: int, b: float, c: str):
		pass

	return SomeTypedPrototype


@pytest.fixture
def typed_inpt():
	def UserTypedInpt(a: float, b: str, c: set):
		pass

	return UserTypedInpt
