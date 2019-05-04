from django.contrib.auth.models import User

from rest_framework import serializers

from consult.models import Theme, Specialist, TimeSlot, Enroll, Method


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = '__all__'


class SpecialistSerializer(serializers.ModelSerializer):
    themes = ThemeSerializer(many=True, read_only=True)

    class Meta:
        model = Specialist
        fields = '__all__'


class TimeSlotSerializer(serializers.ModelSerializer):
    #specialist = SpecialistSerializer(many=False, read_only=True)
    videoconf_url = serializers.ReadOnlyField()
    enrolls = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = TimeSlot
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'password')
        write_only_fields = ('password',)


class EnrollSerializer(serializers.ModelSerializer):
    timeslot = TimeSlotSerializer(many=False, read_only=True)
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Enroll
        fields = '__all__'


class MethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Method
        fields = '__all__'
