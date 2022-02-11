### graphene-gis

[![CircleCI](https://circleci.com/gh/EverWinter23/graphene-gis.svg?style=shield)](https://circleci.com/gh/EverWinter23/graphene-gis)

### INSTALLATION

`django==2.2` is supported. Install the `graphene-gis` with pip:

```bash
$ pip install graphene-gis
```

Make sure that you have appropriate driver to interact with postgis-- `psycopg2` or
`psycopg2-binary`. The binary package is a practical choice for development and testing
but in production it is advised to use the package built from sources. More info [here](https://www.psycopg.org/articles/2018/02/08/psycopg-274-released/).

Add it to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'graphene_gis',
]
```

### USAGE

Hi, check this-> [geoql](https://github.com/EverWinter23/geoql) project out,
it demonstrates usage-- such as querying, mutations using `WKT` and `geojson`.
I will be adding more stuff soon such as containerization, interactive UI etc,
and more examples that showcases the library. This project provides an insight
into real-world usage of the library, do check it out.

This extension can works out of the box with `WKT`, but if you want to use
`GeoJSON` for input while mutations, install `rest_framework_gis` alongside
it-- or check out `geoql` sample project.

#### QUERY

**models.py**

```python
from django.contrib.gis.db import models


class Place(models.Model):
    name = models.CharField(max_length=255)
    location = models.PointField()

```

**schema.py**

```python
from graphene_django import DjangoObjectType
from graphene_gis.converter import gis_converter  # noqa

class PlaceType(DjangoObjectType):
    class Meta:
        model = Place

class Query(graphene.ObjectType):
    place = graphene.Field(Place)

    def resolve_place(self, info):
        return Place(name="San Andreas", location="POINT(34.2 54.3)")

schema = graphene.Schema(query=Query)
```

**Query**

```
query {
    place {
        name
        location
    }
}
```

**Query Output**

```json
"place": {
    "name": "San Andreas",
    "location": {
        "type": "Point",
        "coordinates": [34.2, 54.3]
    }
}
```

#### MUTATION

**schema.py**

```python
class PointModelType(graphene.ObjectType):
    location = graphene.Field(graphene.String, to=scalars.PointScalar())

class CreatePointModelType(graphene.Mutation):
    point = graphene.Field(PointModelType)

    class Arguments:
        location = graphene.Argument(scalars.PointScalar)

    def mutate(root, info, location):
        point = PointModelType(location=location)
        return CreatePointModelType(point=point)
```

**Mutation**

```
mutation {
    createPoint (location: "POINT(3 5)") {
        point {
            location
        }
    }
}
```

**Mutation Output**

```json
"createPoint": {
    "point": {
        "location": "{'type': 'Point', 'coordinates': [3.0, 5.0]}"
    }
}
```

#### EXTRA STUFF

A JSON Converter, so if you're familiar with `graphene`, you know that
it sends `JSONField` as stringified JSON, but with a lot of data, you
dont want to parse it in the frontend, I know it goes against having a
static type, but if you're not modifying the data on the frontend, plus
you're using `typescript` which enforces types anyway, it works like a
charm.

And geojson contains `JSONField` like properties section, and parsing
every node in the frontend is cumbersome if you have ~9000 entries, also
time consuming.

Output without using `json_converter`

```json
{
  "data": {
    "vectors": [
      {
        "type": "Feature",
        "properties": "{\"Name\": \"Blues\", \"area\": 0.0006971253332413299, \"bbox\": [74.59639001261124, 24.7077612714826, 74.61615129922414, 24.755648349214077], \"perimeter\": 0.15862406542812008}",
        "geometry": {
          "type": "Polygon",
          "coordinates": [...]
        }
      }
    ]
  }
}
```

Now if you're working with GeoJSON, you're not working with just one vector,
you're probably working with thousands. Voila `json_converter`!!! Now you can
plot it directly, if you store it in such a way! I won't go into how to structure
the model, but this is fairly accurate description of `GeoJSON`, and anyone
familiar with `django` will be able to reproduce it without issues.

```json
{
  "data": {
    "allVectors": [
      {
        "type": "Feature",
        "properties": {
          "Name": "Blues",
          "area": 0.0006971253332413299,
          "bbox": [
            74.59639001261124,
            24.7077612714826,
            74.61615129922414,
            24.755648349214077
          ],
          "perimeter": 0.15862406542812008
        },
        "geometry": {
          "type": "Polygon",
          "coordinates": [...]
        }
      }
    ]
  }
}
```

### AUTHOR

Rishabh Mehta <eternal.blizzard23@gmail.com>

If you have any issues or queries regarding acadbot, please don't
hesitate to email the **@author**. I have a lot of free time.

I forget stuff, this section is for anyone who wants to build the package.

```bash
$ python setup.py sdist
$ twine upload dist/*
```

### UPDATE

Targeting graphene-v3 update by March'22.

### LICENSE [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This code falls under the MIT license which permits the reuse of the proprietary software provided that all copies of the licensed software include a copy of the MIT License terms and the copyright notice. Go crazy!
