import pytest

from pyprototypes.ParamChecker import OptionsMatcher


def test_match():
	params = ["Hello", "World"]
	matcher = OptionsMatcher(params)
	print(matcher.match("Hell"))
	for i in matcher.match("Hell"):
		if not isinstance(i, str):
			pytest.fail("Output of optionmatcher is NOT all strings!")
