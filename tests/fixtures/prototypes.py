import pytest

from pyprototypes import Prototype


@pytest.fixture
def base_prototype():
	@Prototype
	def proto(potato, pizza): ...

	return proto


@pytest.fixture
def fixture_prototype():
	@Prototype
	def proto_fixtures(potato, pizza): ...

	@proto_fixtures.fixture
	def depth():
		return 42

	@proto_fixtures.fixture
	def potato(depth):
		return depth

	@proto_fixtures.fixture
	def pizza():
		return 62

	return proto_fixtures


@pytest.fixture
def typed_prototype():
	@Prototype.typed
	def proto_fixtures(potato: int, pizza: float): ...

	return proto_fixtures
