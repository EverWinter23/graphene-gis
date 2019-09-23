import json
import graphene
from graphene_gis.converter import gis_converter  # noqa
from graphene_gis.tests.mocks import PointModel, PointModelType


def test_should_convert_gis_scalar_to_geojson():
    class Query(graphene.ObjectType):
        point_model = graphene.Field(PointModelType)

        def resolve_point_model(self, info):
            return PointModel(location="POINT(34.2 54.3)")

    schema = graphene.Schema(query=Query)

    query = """
        query {
            pointModel {
                location
            }
        }
    """

    expected = {
        "pointModel": {
            "location": {
                "type": "Point",
                "coordinates": [34.2, 54.3]
            }
        }
    }

    result = schema.execute(query)
    assert not result.errors
    assert json.loads(json.dumps(dict(result.data))) == expected


def test_should_convert_json_to_dict():
    class Query(graphene.ObjectType):
        point_model = graphene.Field(PointModelType)

        def resolve_point_model(self, info):
            return PointModel(location="POINT(34.2 54.3)",
                              props={"type": "Feature"})

    schema = graphene.Schema(query=Query)

    query = """
        query {
            pointModel {
                location
                props
            }
        }
    """

    expected = {
        "pointModel": {
            "location": {
                "type": "Point",
                "coordinates": [34.2, 54.3]
            },
            "props": {
                "type": "Feature"
            }
        }
    }

    result = schema.execute(query)
    assert not result.errors
    assert json.loads(json.dumps(dict(result.data))) == expected
