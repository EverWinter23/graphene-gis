import json

import graphene
from django.contrib.gis.geos import GEOSGeometry
from graphene_gis.converter import gis_converter  # noqa
from graphene_gis.scalars import PointScalar
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


"""
NOTE: Refer https://github.com/EverWinter23/graphene-gis/issues/9
Some evasive issue. I wouldn't reccomend using the following for
implementing mutations, because it involves some unecessary steps.

The converter will convert the WKT geometry to geojson, which you'll
have to convert back to WKT using GEOSGeometry to initialize the object.

It's way simple rather use the graphene.String for the input argument for 
WKT inputs. This is demonstarted in the next test case.
"""
def test_scalar_query_variables():
    class Query(graphene.ObjectType):
        point_model = graphene.Field(PointModelType, location=PointScalar(required=True))

        def resolve_point_model(self, info, location):
            return PointModel(location=GEOSGeometry(f"{location}"), props={"type": "Feature"})

    schema = graphene.Schema(query=Query)

    query = """
        query TestQuery($location: PointScalar!) {
            pointModel(location: $location) {
                location
                props
            }
        }
    """

    expected = {
        "pointModel": {
            "location": {
                "type": "Point",
                "coordinates": [42.0, 15.0]
            },
            "props": {
                "type": "Feature"
            }
        }
    }

    result = schema.execute(query, variables={"location": "POINT(42.0 15.0)"})
    assert not result.errors
    assert json.loads(json.dumps(dict(result.data))) == expected


def test_native_query_variables():
    class Query(graphene.ObjectType):
        point_model = graphene.Field(PointModelType, location=graphene.String(required=True))

        def resolve_point_model(self, info, location):
            return PointModel(location=location, props={"type": "Feature"})

    schema = graphene.Schema(query=Query)

    query = """
        query TestQuery($location: String!) {
            pointModel(location: $location) {
                location
                props
            }
        }
    """

    expected = {
        "pointModel": {
            "location": {
                "type": "Point",
                "coordinates": [42.0, 15.0]
            },
            "props": {
                "type": "Feature"
            }
        }
    }

    result = schema.execute(query, variables={"location": "POINT(42.0 15.0)"})
    assert not result.errors
    assert json.loads(json.dumps(dict(result.data))) == expected
