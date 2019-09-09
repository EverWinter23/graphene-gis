from graphql.language import ast
from graphene.types import Scalar
from django.contrib.gis.geos import GEOSGeometry
import pdb


class GISScalar(Scalar):
    @property
    def geom_typeid(self):
        raise NotImplementedError(
            "GEOSScalar is an abstract class and doesn't have a 'geom_typeid'. \
            Instantiate a concrete subtype instead."
        )

    @staticmethod
    def serialize(geometry):
        return eval(geometry.geojson)

    @classmethod
    def parse_literal(cls, node):
        # pdb.set_trace()
        assert isinstance(node, ast.StringValue)
        geometry = GEOSGeometry(node.value)
        return eval(geometry.geojson)

    @classmethod
    def parse_value(cls, node):
        pdb.set_trace()
        geometry = GEOSGeometry(node.value)
        return eval(geometry.geojson)


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
