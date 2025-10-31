import pytest

from pyprototypes.arguments import ArgChecker
from pyprototypes.exceptions import UnsupportedParameters
from pyprototypes.signature import SignatureInspect


def prototype(monkey: float, money: str, gorilla: int): ...


def inpt(mnkey: int, money: str, gorilla: str): ...


def test_machine_success():
	signature = SignatureInspect.fetch(prototype)
	matcher = ArgChecker(True)
	assert matcher.match(signature, signature)


def test_machine_fail():
	signature = SignatureInspect.fetch(prototype)
	inpt_sig = SignatureInspect.fetch(inpt)
	matcher = ArgChecker(typed=True)
	with pytest.raises(
		UnsupportedParameters,
		match=r".*Parameter 'mnkey' is not supported.*",
	):
		assert not matcher.match(signature, inpt_sig)
