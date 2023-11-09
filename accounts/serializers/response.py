from rest_framework import serializers
from ..models import Doctor, No_covered, Opening_hour


class DoctorShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('name',)
