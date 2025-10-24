import pytest


@pytest.fixture
def correct_names():
	return {"monkey": float, "money": str, "gorilla": int}


@pytest.fixture
def odd_names():
	return {"money": int, "dog": str, "gorilla": int}  # dog is the odd one
