import graphene
from graphene_django import DjangoObjectType

from consult.models import Specialist, TimeSlot


class SpecialistType(DjangoObjectType):
    class Meta:
        model = Specialist


class TimeSlotType(DjangoObjectType):
    class Meta:
        model = TimeSlot


class Query(graphene.ObjectType):
    specialists = graphene.List(SpecialistType)
    timeslots = graphene.List(TimeSlotType)

    def resolve_specialists(self, info):
        return Specialist.objects.all()

    def resolve_timeslots(self,info):
        return TimeSlot.objects.select_related('enrolls').all()

