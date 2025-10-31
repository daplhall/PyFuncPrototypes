import pytest

import pyprototypes
from pyprototypes import PrototypeCode, exceptions


def test_prototype_success(base_prototype):
	@base_prototype.function
	def inpt(potato, pizza): ...

	assert base_prototype.check(inpt) == PrototypeCode.OK


def test_prototype_name_fail(base_prototype):
	with pytest.raises(
		exceptions.UnsupportedParameters,
		match=(
			r".* Parameter 'potat' is not supported, did you mean:\n"
			r"\t- potato\n.*"
			r".* Parameter 'piz' is not supported, did you mean:\n"
			r"\t- pizza\n.*"
		),
	):

		@base_prototype.function
		def inpt(potat, piz): ...


def test_prototype_type_failure(typed_prototype):
	with pytest.raises(
		exceptions.UnsupportedParameters,
		match=(
			r".* Wrong Type - Parameter 'pizza'\n"
			r"\t it is 'int' it should be 'float.*'\n"
			r".* Wrong Type - Parameter 'potato'\n"
			r"\t it is 'float' it should be 'int'\n.*"
		),
	):

		@typed_prototype.function
		def inpt(pizza: int, potato: float): ...


def test_fixture_fixtures_success(fixture_prototype):
	@fixture_prototype.function
	def inpt(pizza, potato):
		return pizza + potato

	assert fixture_prototype.check(inpt) == pyprototypes.PrototypeCode.OK
	assert inpt() == 104
