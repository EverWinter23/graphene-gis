.PHONY: tests
tests:
	py.test graphene_gis --cov=graphene_gis -vv


.PHONY: lint
lint:
	flake8 graphene_gis


.PHONY: format
format:
	black graphene_gis
