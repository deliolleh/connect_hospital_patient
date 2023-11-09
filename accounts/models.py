from django.db import models


# Create your models here.
class Patient(models.Model):
    name = models.CharField(max_length=20)


class Doctor(models.Model):
    name = models.CharField(max_length=20)
    hospital = models.CharField(max_length=50)
    department = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class No_covered(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, blank=False, null=False, related_name='nocovers')
    subject = models.CharField(max_length=100)


class Opening_hour(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, blank=False, null=False, related_name='opentimes')
    day = models.IntegerField()
    work = models.BooleanField()
    lunch = models.BooleanField()
    start = models.CharField(max_length=4)
    end = models.CharField(max_length=4)
    lunch_start = models.CharField(max_length=4)
    lunch_end = models.CharField(max_length=4)
