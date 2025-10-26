import pytest

import pyprototypes.exceptions as exceptions


def test_prototype_success(base_prototype):
	def inpt(potato, pizza): ...

	assert base_prototype.check(inpt) == inpt


def test_prototype_name_fail(base_prototype):
	def inpt(potat, piz): ...

	with pytest.raises(
		exceptions.UnsupportedParameters,
		match=r".*Parameter 'potat' is not supported, did you mean:.*",
	):
		base_prototype.check(inpt)


def test_prototype_type_failure(typed_prototype):
	def inpt(pizza: int, potato: float): ...

	with pytest.raises(
		exceptions.UnsupportedParameters,
		match=r".*Wrong Type - Parameter 'pizza'.*",
	):
		typed_prototype.check(inpt)


def test_fixture_fixtures_success(fixture_prototype):
	def inpt(pizza, potato):
		return pizza + potato

	p = fixture_prototype.check(inpt)
	assert p() == 104
