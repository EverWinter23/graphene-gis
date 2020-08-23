import json
import graphene
from graphene_gis import scalars


def test_should_mutate_gis_scalar_using_parse_literal():
    class PointModelType(graphene.ObjectType):
        location = graphene.Field(graphene.JSONString, to=scalars.PointScalar())

    class Query(graphene.ObjectType):
        hello_world = graphene.String()

        def resolve_hello_world(self, info):
            return "hello, world!"

    class CreatePointModelType(graphene.Mutation):
        point = graphene.Field(PointModelType)

        class Arguments:
            location = graphene.Argument(scalars.PointScalar)

        def mutate(root, info, location):
            point = PointModelType(location=location)
            return CreatePointModelType(point=point)

    class TestMutation(graphene.ObjectType):
        create_point = CreatePointModelType.Field()

    schema = graphene.Schema(query=Query, mutation=TestMutation)

    query = """
        mutation {
            createPoint (location: "POINT(3 5)") {
                point {
                    location
                }
            }
        }
    """

    expected = {
        "createPoint": {
            "point": {"location": '{"type": "Point", "coordinates": [3.0, 5.0]}'}
        }
    }

    result = schema.execute(query)
    assert not result.errors
    assert json.loads(json.dumps(dict(result.data))) == expected


def test_should_mutate_json_scalar_using_parse_literal():
    # NOTE: When mutations are done using REST Serializers, all
    # Fields will be iterpreted as "is" without the use of scalars.
    # When querying the data, the scalars will be made use of, but,
    # while performing mutations through the Serializers, do not
    # make use of the scalars, therefore you need not implement
    # parse_literal and parse_value.
    class JSONModelType(graphene.ObjectType):
        props = graphene.Field(graphene.JSONString, to=scalars.JSONScalar())

    class Query(graphene.ObjectType):
        hello_world = graphene.String()

        def resolve_hello_world(self, info):
            return "hello, world!"

    class JSONMutation(graphene.Mutation):
        json = graphene.Field(JSONModelType)

        class Arguments:
            props = graphene.Argument(graphene.JSONString)

        def mutate(root, info, props):
            json = JSONModelType(props=props)
            return JSONMutation(json=json)

    class Mutation(graphene.ObjectType):
        create_json = JSONMutation.Field()

    schema = graphene.Schema(query=Query, mutation=Mutation)

    mutation = """
        mutation JSONMutation{
            createJson (props: "{\\"type\\": \\"Feature\\"}") {
                json {
                    props
                }
            }
        }
    """
    expected = {
        "createJson": {
            "json": {
                "props": '{"type": "Feature"}'
            }
        }
    }

    result = schema.execute(mutation)
    assert not result.errors
    assert json.loads(json.dumps(dict(result.data))) == expected
