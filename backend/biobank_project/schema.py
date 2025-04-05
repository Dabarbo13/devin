import graphene
import users.schema
import clinical_trials.schema
import donation_management.schema
import recruiting.schema
import sponsor_portal.schema
import web_store.schema

class Query(
    users.schema.Query,
    clinical_trials.schema.Query,
    donation_management.schema.Query,
    recruiting.schema.Query,
    sponsor_portal.schema.Query,
    web_store.schema.Query,
    graphene.ObjectType
):
    pass

class Mutation(
    users.schema.Mutation,
    clinical_trials.schema.Mutation,
    donation_management.schema.Mutation,
    recruiting.schema.Mutation,
    sponsor_portal.schema.Mutation,
    web_store.schema.Mutation,
    graphene.ObjectType
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
