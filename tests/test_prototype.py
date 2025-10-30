import pytest

import pyprototypes.exceptions as exceptions


def test_prototype_success(base_prototype):
	@base_prototype.function
	def inpt(potato, pizza): ...

	assert base_prototype.check(inpt)


def test_prototype_name_fail(base_prototype):
	with pytest.raises(
		exceptions.UnsupportedParameters,
		match=r".*Parameter 'potat' is not supported, did you mean:.*",
	):

		@base_prototype.function
		def inpt(potat, piz): ...


def test_prototype_type_failure(typed_prototype):
	with pytest.raises(
		exceptions.UnsupportedParameters,
		match=r".*Wrong Type - Parameter 'pizza'.*",
	):

		@typed_prototype.function
		def inpt(pizza: int, potato: float): ...


def test_fixture_fixtures_success(fixture_prototype):
	@fixture_prototype.function
	def inpt(pizza, potato):
		return pizza + potato

	assert fixture_prototype.check(inpt)
	assert inpt() == 104
