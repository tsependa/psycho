from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import viewsets

from consult.models import Theme, Specialist, TimeSlot, Enroll, Method
from consult.serializers import ThemeSerializer, SpecialistSerializer, TimeSlotSerializer, EnrollSerializer, \
    UserSerializer, MethodSerializer


class ThemeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer


class SpecialistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializer

    def get_queryset(self):
        queryset = Specialist.objects.all().filter(active=True)
        return queryset


class TimeslotFilteredViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = TimeSlot.objects.all()
        specialist_id = self.kwargs['specialist_id']
        if specialist_id is not None:
            queryset = queryset.filter(specialist_id=specialist_id).filter(start_time__gte=datetime.now()).exclude(
                enroll__isnull=False)
        return queryset


class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer


class EnrollViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Enroll.objects.all()
    serializer_class = EnrollSerializer

    def get_queryset(self):
        queryset = Enroll.objects.all()
        user = self.request.user
        if user is not None:
            queryset = queryset.filter(user=user)
        return queryset


class EnrollSpecViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Enroll.objects.all()
    serializer_class = EnrollSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MethodViewSet(viewsets.ModelViewSet):
    queryset = Method.objects.all()
    serializer_class = MethodSerializer
