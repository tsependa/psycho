from rest_framework import routers

from consult.views import YandexNotification
from consult.viewsets import ThemeViewSet, SpecialistViewSet, TimeslotFilteredViewSet, EnrollViewSet, UserViewSet, \
    EnrollSpecViewSet, MethodViewSet, TimeSlotViewSet

router = routers.DefaultRouter()

router.register(r'theme', ThemeViewSet)
router.register(r'specialist', SpecialistViewSet)
router.register(r'method', MethodViewSet)
router.register(r'timeslot', TimeSlotViewSet)
router.register(r'timeslots/(?P<specialist_id>.+)', TimeslotFilteredViewSet, base_name='TimeSlot')

router.register(r'enroll', EnrollViewSet, base_name='Enroll')
router.register(r'enrollspec', EnrollSpecViewSet, base_name='EnrollSpec')

router.register(r'user', UserViewSet)



