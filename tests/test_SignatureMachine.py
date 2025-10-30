import pytest

from pyprototypes.BaseMatchers import Signature
from pyprototypes.exceptions import UnsupportedParameters
from pyprototypes.SignatureMachine import SignatureMachine


def prototype(monkey: float, money: str, gorilla: int): ...


def inpt(mnkey: int, money: str, gorilla: str): ...


def test_machine_success():
	signature = Signature.signature(prototype)
	matcher = SignatureMachine(True)
	assert matcher.match(signature, signature)


def test_machine_fail():
	signature = Signature.signature(prototype)
	inpt_sig = Signature.signature(inpt)
	matcher = SignatureMachine(is_typed=True)
	with pytest.raises(
		UnsupportedParameters,
		match=r".*Parameter 'mnkey' is not supported.*",
	):
		assert not matcher.match(signature, inpt_sig)
