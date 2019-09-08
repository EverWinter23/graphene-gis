from django.contrib.gis.db import models as gis_models
from graphene_gis import scalars
from graphene_gis.converter import gis_converter
from graphene_django.tests.test_converter import assert_conversion


def test_should_date_point_field_to_point_scalar():
    assert_conversion(gis_models.PointField, scalars.PointScalar)


def test_should_date_point_field_to_line_string_scalar():
    assert_conversion(gis_models.LineStringField, scalars.LineStringScalar)
