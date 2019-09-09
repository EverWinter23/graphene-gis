from django.contrib.gis.db import models as gis_models
from graphene_django.converter import convert_django_field
from graphene_gis import scalars

GIS_FIELD_SCALAR = {
    "PointField": scalars.PointScalar,
    "LineStringField": scalars.LineStringScalar,
    "PolygonField": scalars.PolygonScalar,
}


@convert_django_field.register(gis_models.PolygonField)
@convert_django_field.register(gis_models.LineStringField)
@convert_django_field.register(gis_models.PointField)
def gis_converter(field, registry=None):
    class_name = field.__class__.__name__
    return GIS_FIELD_SCALAR[class_name](
        required=not field.null, description=field.help_text
    )
