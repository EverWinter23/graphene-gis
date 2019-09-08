import graphene
from graphene_gis import scalars


def test_should_mutate_gis_scalar_using_parse_literal():
    class PointModelType(graphene.ObjectType):
        point = graphene.Field(graphene.String, to=scalars.PointScalar())

    class CreatePointModelType(graphene.Mutation):
        person = graphene.Field(PointModelType)

        class Arguments:
            point = graphene.Argument(scalars.PointScalar)

        def mutate(root, info, point):
            person = PointModelType(point=point)
            return CreatePointModelType(person=person)

    class TestMutation(graphene.ObjectType):
        create_person = CreatePointModelType.Field()

    schema = graphene.Schema(mutation=TestMutation)

    query = """
        mutation {
            createPerson(point:"POINT(3 5)") {
                person {
                    point
                }
            }
        }
    """

    expected = {
        "createPerson": {
            "person": {"point": "{'type': 'Point', 'coordinates': [3.0, 5.0]}"}
        }
    }

    result = schema.execute(query)
    assert not result.errors
    assert result.data == expected
