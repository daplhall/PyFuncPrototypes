from pyprototypes.BaseMatchers import NameMatcher, TypeMatcher


def test_NameMatcher_match(correct_names):
	closest_match = NameMatcher.match_str(correct_names, "monky")
	assert closest_match == ["money", "monkey"]


def test_NameMatcher_has_oddities(correct_names, odd_names):
	assert NameMatcher.has_oddities(correct_names, odd_names)


def test_NameMatcher_not_has_oddities(correct_names):
	assert not NameMatcher.has_oddities(correct_names, correct_names)
