import pytest
from graphene_gis import scalars


def test_base_scalar():
    with pytest.raises(NotImplementedError):
        base_scalar = scalars.GISScalar()
        assert base_scalar.geom_typeid is not None
