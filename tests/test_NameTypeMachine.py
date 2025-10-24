import pytest

from pyprototypes.BaseMatchers import Signature
from pyprototypes.exceptions import UnsupportedParameters
from pyprototypes.NameTypeMatcher import MatcherMachine


def prototype(monkey: float, money: str, gorilla: int):
	pass


def inpt(mnkey: int, money: str, gorilla: str):
	pass


def test_machine_success():
	signature = Signature.signature(prototype)
	meta = Signature.metadata(prototype)
	matcher = MatcherMachine()
	assert matcher.match(signature, signature, meta, True)


def test_machine_fail():
	signature = Signature.signature(prototype)
	inpt_sig = Signature.signature(inpt)
	meta = Signature.metadata(inpt)
	matcher = MatcherMachine()
	with pytest.raises(UnsupportedParameters):
		assert not matcher.match(signature, inpt_sig, meta, True)
