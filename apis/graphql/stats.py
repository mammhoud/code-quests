import graphene
from graphene_django import DjangoObjectType
from graphene import Field, List, ID, Int
from ..models import Stat
from core.models import Profile


class StatType(DjangoObjectType):
    class Meta:
        model = Stat
        fields = "__all__"


class Query(graphene.ObjectType):
    all_stats = List(StatType)
    stat_by_profile = Field(StatType, profile_id=ID(required=True))
    top_stats_by_evaluation = List(StatType, limit=Int(default_value=10))

    def resolve_all_stats(root, info):
        return Stat.objects.all()

    def resolve_stat_by_profile(root, info, profile_id):
        return Stat.objects.get(profile_id=profile_id)

    def resolve_top_stats_by_evaluation(root, info, limit):
        return Stat.objects.order_by("-evaluation")[:limit]


class CreateStat(graphene.Mutation):
    class Arguments:
        profile_id = ID(required=True)
        total_exercises = Int()
        total_workouts = Int()
        evaluation = Int()

    stat = Field(StatType)

    # @classmethod
    def mutate(self, info, profile_id, total_exercises=0, total_workouts=0, evaluation=0):
        profile = Profile.objects.get(id=profile_id)
        stat = Stat.objects.create(
            profile=profile,
            total_exercises=total_exercises,
            total_workouts=total_workouts,
            evaluation=evaluation
        )
        return CreateStat(stat=stat)


class Mutation(graphene.ObjectType):
    create_stat = CreateStat.Field()
