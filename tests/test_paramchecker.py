import pytest

from pyprototypes.ParamChecker import ParamChecker, UnsupportedParameters


def test_basic_prototype(abc_prototype):
	matcher = ParamChecker(abc_prototype)
	try:
		assert matcher.check(abc_prototype) == {"a", "b", "c"}
	except UnsupportedParameters:
		pytest.fail("Checker failed on perfect match")


def test_basic_prototype_raise(abc_prototype, abp_inpt):
	matcher = ParamChecker(abc_prototype)
	with pytest.raises(UnsupportedParameters):
		matcher.check(abp_inpt)


def test_typed_prototype(typed_prototype):
	matcher = ParamChecker.with_typing(typed_prototype)
	try:
		assert matcher.check(typed_prototype) == {"a", "b", "c"}
	except UnsupportedParameters:
		pytest.fail("Typed Checker failed on perfect match")


def test_typed_prototype_error(typed_prototype, typed_inpt):
	matcher = ParamChecker.with_typing(typed_prototype)
	with pytest.raises(UnsupportedParameters):
		matcher.check(typed_inpt)
