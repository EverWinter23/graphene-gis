import graphene
from graphene_gis.converter import gis_converter
from graphene_django import DjangoObjectType


def test_should_convert_gis_scalar_to_geojson():
    from graphene_gis.tests.models import PointModel

    class PointModelType(DjangoObjectType):
        class Meta:
            model = PointModel

    class Query(graphene.ObjectType):
        point_model = graphene.Field(PointModelType)

        def resolve_point_model(self, info):
            return PointModel(point="POINT(34.2 54.3)")

    schema = graphene.Schema(query=Query)

    query = """
        query {
            pointModel {
                point
            }
        }
    """

    expected = {"pointModel": {"point": {"type": "Point", "coordinates": [34.2, 54.3]}}}

    result = schema.execute(query)
    assert not result.errors
    assert result.data == expected
