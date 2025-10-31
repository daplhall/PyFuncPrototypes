import pytest

from pyprototypes.signature import (
	SigMeta,
	SignatureConstructed,
	SignatureInspect,
)


@pytest.mark.parametrize("fetcher", [SignatureConstructed, SignatureInspect])
def test_kwargs(kwargs_only, fetcher):
	data: SigMeta = fetcher.fetch(kwargs_only)
	assert data.name == kwargs_only.__name__
	assert data.func == kwargs_only
	assert data.signature == {"bar": int, "foo": str}
	assert data.positionals == {}


@pytest.mark.parametrize("fetcher", [SignatureConstructed, SignatureInspect])
def test_positional(with_positional, fetcher):
	data: SigMeta = fetcher.fetch(with_positional)
	assert data.name == with_positional.__name__
	assert data.func == with_positional
	assert data.signature == {"bar": int, "foo": str}
	assert data.positionals == {"bar": int}
