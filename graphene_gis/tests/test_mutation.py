import graphene
from graphene_gis import scalars


def test_should_mutate_gis_scalar_using_parse_literal():
    class PointModelType(graphene.ObjectType):
        location = graphene.Field(graphene.String, to=scalars.PointScalar())

    class CreatePointModelType(graphene.Mutation):
        point = graphene.Field(PointModelType)

        class Arguments:
            location = graphene.Argument(scalars.PointScalar)

        def mutate(root, info, location):
            point = PointModelType(location=location)
            return CreatePointModelType(point=point)

    class TestMutation(graphene.ObjectType):
        create_point = CreatePointModelType.Field()

    schema = graphene.Schema(mutation=TestMutation)

    query = """
        mutation {
            createPoint(location:"POINT(3 5)") {
                point {
                    location
                }
            }
        }
    """

    expected = {
        "createPointc": {
            "point": {"location": "{'type': 'Point', 'coordinates': [3.0, 5.0]}"}
        }
    }

    result = schema.execute(query)
    assert not result.errors
    assert result.data == expected


def test_should_mutate_gis_scalar_using_parse_literal():
    class PointModelType(graphene.ObjectType):
        location = graphene.Field(graphene.String, to=scalars.PointScalar())
        properties = graphene.Field(
            graphene.JSONString, to=scalars.JSONScalar())

    class CreatePointModelType(graphene.Mutation):
        point = graphene.Field(PointModelType)

        class Arguments:
            location = graphene.Argument(scalars.PointScalar)
            properties = graphene.Argument(scalars.JSONScalar)

        def mutate(root, info, location, properties):
            point = PointModelType(location=location,
                                   properties=properties)
            return CreatePointModelType(point=point)

    class TestMutation(graphene.ObjectType):
        create_point = CreatePointModelType.Field()

    schema = graphene.Schema(mutation=TestMutation)

    query = """
        mutation {
            createPoint(location:"POINT(3 5)", properties:"{\"string\": \"value\"}") {
                point {
                    location
                    properties
                }
            }
        }
    """

    expected = {
        "createPointc": {
            "point": {"location": "{'type': 'Point', 'coordinates': [3.0, 5.0]}"}
        }
    }

    result = schema.execute(query)
    import pdb
    pdb.set_trace()
    assert not result.errors
    assert result.data == expected
