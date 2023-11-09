from rest_framework import serializers
from accounts.models import Patient, Doctor
from .models import Diagnosis


class DiagnosisCreatedSerializer(serializers.ModelSerializer):
    class PatientSerializer(serializers.ModelSerializer):
        class Meta:
            model = Patient
            fields = ('pk', 'name')

    class DoctorSerializer(serializers.ModelSerializer):
        class Meta:
            model = Doctor
            fields = ('pk', 'name')

    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = Diagnosis
        fields = ('pk', 'patient', 'doctor', 'accepted', 'wanted_time', 'expired_time')
        read_only_fields = ('patient', 'doctor')


class DiagnosisShowSerializer(serializers.ModelSerializer):
    class PatientSerializer(serializers.ModelSerializer):
        class Meta:
            model = Patient
            fields = ('name',)

    patient = PatientSerializer()

    class Meta:
        model = Diagnosis
        fields = ('pk', 'patient', 'wanted_time', 'expired_time')


class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = ('pk', 'patient', 'wanted_time', 'expired_time', 'accepted')
