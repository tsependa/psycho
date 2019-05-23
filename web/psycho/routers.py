from rest_framework import routers

from consult.viewsets import ThemeViewSet, SpecialistViewSet, TimeslotAvailableViewSet, EnrollViewSet, UserViewSet, \
    EnrollSpecViewSet, MethodViewSet, TimeSlotViewSet, TimeslotSpecialistViewSet

router = routers.DefaultRouter()

router.register(r'theme', ThemeViewSet)
router.register(r'specialist', SpecialistViewSet)
router.register(r'method', MethodViewSet)
router.register(r'timeslot', TimeSlotViewSet)
router.register(r'timeslots/(?P<specialist_id>.+)', TimeslotAvailableViewSet, base_name='TimeSlot')
router.register(r'timeslots_all/(?P<specialist_id>.+)', TimeslotSpecialistViewSet, base_name='TimeSlot')
router.register(r'enroll', EnrollViewSet, base_name='Enroll')
router.register(r'enrollspec', EnrollSpecViewSet, base_name='EnrollSpec')

router.register(r'user', UserViewSet)


