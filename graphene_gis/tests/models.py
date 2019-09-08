from django.contrib.gis.db import models as gis_models


class PointModel(gis_models.Model):
    point = gis_models.PointField()


class LineStringModel(gis_models.Model):
    line_string = gis_models.LineStringField()
