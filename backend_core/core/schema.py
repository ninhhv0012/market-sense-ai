import graphene
import analysis.schema

# Kế thừa Query và Mutation từ app analysis
class Query(analysis.schema.Query, graphene.ObjectType):
    pass

class Mutation(analysis.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)