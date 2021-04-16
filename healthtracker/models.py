from django.contrib.auth.models import AbstractUser
from django.db import models

# registration number
def registrationNo():
    latest_patient = Patients.objects.all().order_by('id').last()
    if not latest_patient:
        return "REG20201"
    return f"REG2020{latest_patient.id + 1}"

# Create your models here.

class User(AbstractUser):
    pass

class Patients(models.Model):
    FirstName = models.CharField(max_length=255)
    LastName = models.CharField(max_length=255)
    RegNumber = models.CharField(max_length=255, default=registrationNo, blank=False, null=False)
    RoomNo = models.IntegerField()
    Gender = models.CharField(max_length=6)
    Address = models.CharField(max_length=255)
    TimeOfAdmission = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Name: f{self.FirstName}, Reg Number: f{self.RegNumber}"

    def serialize(self):
        return {
            "regnumber": self.RegNumber,
            "fname": self.FirstName,
            "lname": self.LastName,
            "roomnumber": self.RoomNo,
            "gender": self.Gender,
            "address": self.Address,
            "admissiontime": self.TimeOfAdmission.strftime("%b %d %Y, %I:%M %p")
        }

class PatientsStatus(models.Model):
    Patient = models.ForeignKey('Patients', on_delete=models.CASCADE, related_name="pateint")
    PulseRate = models.FloatField()
    Temperature = models.FloatField()
    Time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Current Status: Pulse: {self.PulseRate}, Temp: f{self.Temperature}"

    def serialize(self):
        return {
            "patient": self.Patient.serialize(),
            "pulserate": self.PulseRate,
            "temperature": self.Temperature,
            "time": self.Time.strftime("%b %d %Y, %I:%M %p")
        }