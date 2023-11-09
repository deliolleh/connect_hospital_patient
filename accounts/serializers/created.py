from rest_framework import serializers
from ..models import Doctor, Patient, No_covered, Opening_hour


class PatientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"


class DoctorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"


class No_coverCreatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = No_covered
        fields = ('pk', 'doctor', 'subject')
        read_only_fields = ('doctor',)


class Opening_HourCreatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opening_hour
        fields = "__all__"
        read_only_fields = ('doctor',)


class DoctorCreateShowSerializer(serializers.ModelSerializer):
    class NoCoveredSerializer(serializers.ModelSerializer):
        class Meta:
            model = No_covered
            fields = ('subject',)

    class OpeningHourSerializer(serializers.ModelSerializer):
        class Meta:
            model = Opening_hour
            fields = ('day', 'work', 'start', 'end', 'lunch', 'lunch_start', 'lunch_end')

    nocovers = NoCoveredSerializer(many=True)
    opentimes = OpeningHourSerializer(many=True)

    class Meta:
        model = Doctor
        fields = ('pk', 'name', 'hospital', 'department', 'nocovers', 'opentimes')