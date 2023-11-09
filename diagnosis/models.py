from django.db import models
from accounts.models import Patient, Doctor


# Create your models here.
class Diagnosis(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    wanted_time = models.DateTimeField()
    expired_time = models.DateTimeField()
