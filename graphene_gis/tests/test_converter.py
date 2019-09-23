from django.contrib.gis.db import models as gis_models
from django.contrib.postgres import fields
from graphene_gis import scalars
from graphene_gis.converter import gis_converter, json_converter  # noqa
from graphene_django.tests.test_converter import assert_conversion


def test_should_date_point_field_to_point_scalar():
    assert_conversion(gis_models.PointField, scalars.PointScalar)


def test_should_date_point_field_to_line_string_scalar():
    assert_conversion(gis_models.LineStringField, scalars.LineStringScalar)


def test_should_json_to_dict():
    assert_conversion(fields.JSONField, scalars.JSONScalar)
