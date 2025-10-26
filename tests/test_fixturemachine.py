import pytest

from pyprototypes.BaseMatchers import Signature
from pyprototypes.exceptions import FixtureNotDefined
from pyprototypes.FixtureMachine import FixtureMachine
from pyprototypes.prototype import Prototype


def test_fixture():
	@Prototype
	def fix(pizza: int, potato: str): ...

	@fix.fixture
	def chips():
		return 60

	@fix.fixture
	def potato():
		return "Hello world"

	@fix.fixture
	def pizza(chips):
		return chips + 2

	def testfunc(pizza: int, potato: str): ...

	machine = FixtureMachine()
	q = machine.match(Signature.signature(testfunc), fix.fixtures)
	assert q == {"pizza": 62, "potato": "Hello world"}


def test_missing_fixture():
	@Prototype
	def fix(pizza: int, potato: str): ...

	def chips(): ...
	@fix.fixture
	def potato(chips): ...
	def testfunc(potato: str): ...

	machine = FixtureMachine()
	with pytest.raises(
		FixtureNotDefined,
		match="Fixture 'chips' is not defined\n",
	):
		machine.match(Signature.signature(testfunc), fix.fixtures)
