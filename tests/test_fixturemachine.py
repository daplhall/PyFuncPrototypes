import pytest

from pyprototypes.exceptions import FixtureNotDefined
from pyprototypes.fixtures import FixFinder
from pyprototypes.prototype import Prototype
from pyprototypes.signature import SignatureInspect


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

	machine = FixFinder()
	q = machine.match(SignatureInspect.fetch(testfunc), fix._fixtures)
	assert q == {"pizza": 62, "potato": "Hello world"}


def test_missing_fixture():
	@Prototype
	def fix(pizza: int, potato: str): ...

	def chips(): ...
	@fix.fixture
	def potato(chips): ...
	def testfunc(potato: str): ...

	machine = FixFinder()
	with pytest.raises(
		FixtureNotDefined,
		match="Fixture 'chips' is not defined\n",
	):
		machine.match(SignatureInspect.fetch(testfunc), fix._fixtures)
