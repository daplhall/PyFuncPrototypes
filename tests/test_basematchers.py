from pyprototypes.BaseMatchers import NameMatcher, TypeMatcher


def test_NameMatcher_match(correct_names):
	closest_match = NameMatcher.match_str(correct_names, "monky")
	assert closest_match == ["money", "monkey"]


def test_NameMatcher_is_odd(correct_names, odd_names):
	assert NameMatcher.is_odd(correct_names, odd_names)


def test_NameMatcher_not_is_odd(correct_names):
	assert not NameMatcher.is_odd(correct_names, correct_names)
