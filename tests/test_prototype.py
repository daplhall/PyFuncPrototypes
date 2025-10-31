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


def test_positionals_correct(positional_prototype):
	def inpt(bar: str, foo: int, /): ...

	fixed = positional_prototype.function(inpt)

	assert fixed == inpt


def test_positionals(positional_prototype):
	with pytest.raises(
		exceptions.UnsupportedParameters,
		match=(
			r".*Positional order is wrong\n"
			r"\t it should be 'bar, foo'\n"
			r"\t but it is 'foo, bar'\n.*"
		),
	):

		@positional_prototype.function
		def inpt(foo: int, bar: str, /): ...


def test_fixture_pos_wrong(fixture_prototype):
	with pytest.raises(
		exceptions.UnsupportedParameters,
		match=(
			r".*Positional order is wrong\n"
			r"\t it should be '\(empty\)'\n"
			r"\t but it is 'pizza'\n.*"
		),
	):

		@fixture_prototype.function
		def inpt(pizza, /, potato):
			return pizza + potato


def test_fixture_pos(fixture_prototype_pos):
	@fixture_prototype_pos.function
	def inpt(potato, /, pizza):
		return pizza + potato

	assert fixture_prototype_pos.check(inpt) == pyprototypes.PrototypeCode.OK
	assert inpt(62) == 104
