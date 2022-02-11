import json
from graphql.language import ast
from graphene.types import Scalar
from django.contrib.gis.geos import GEOSGeometry


class GISScalar(Scalar):
    @property
    def geom_typeid(self):
        raise NotImplementedError(
            "GEOSScalar is an abstract class and doesn't have a 'geom_typeid'. \
            Instantiate a concrete subtype instead."
        )

    @staticmethod
    def serialize(geometry):
        return json.loads(geometry.geojson)

    @classmethod
    def parse_literal(cls, node):
        assert isinstance(node, ast.StringValue)
        geometry = GEOSGeometry(node.value)
        return json.loads(geometry.geojson)

    @classmethod
    def parse_value(cls, node):
        geometry = GEOSGeometry(node)
        return json.loads(geometry.geojson)


class JSONScalar(Scalar):
    @staticmethod
    def serialize(value):
        return value

    @staticmethod
    def parse_literal(cls, node):
        raise NotImplementedError

    @staticmethod
    def parse_value(cls, node):
        raise NotImplementedError


class PointScalar(GISScalar):
    geom_typeid = 0

    class Meta:
        description = "A GIS Point geojson"


class LineStringScalar(GISScalar):
    geom_typeid = 1

    class Meta:
        description = "A GIS LineString geojson"


class PolygonScalar(GISScalar):
    geom_typeid = 3

    class Meta:
        description = " A GIS Polygon geojson"


class MultiPolygonScalar(GISScalar):
    geom_typeid = 6

    class Meta:
        description = " A GIS MultiPolygon geojson"
