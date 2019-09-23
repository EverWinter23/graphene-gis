from django.contrib.gis.db import models as gis_models
from django.contrib.postgres import fields
from graphene_django import DjangoObjectType

from graphene_gis.converter import gis_converter, json_converter  # noqa


class PointModel(gis_models.Model):
    location = gis_models.PointField()
    props = fields.JSONField()


class PointModelType(DjangoObjectType):
    class Meta:
        model = PointModel
