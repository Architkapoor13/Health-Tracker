import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import *

# Create your views here.
from django.urls import reverse


def index(request):
    return render(request, "healthtracker/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "healthtracker/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "healthtracker/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def checkhealth(request):
    if request.method == 'POST':
        regnumber = request.POST["regnumber"]
        try:
            patient = Patients.objects.get(RegNumber=regnumber)
        except Patients.DoesNotExist:
            patient = None
        if patient == None:
            return render(request, "healthtracker/chekhealth.html",{
                "message": "Registration Number not found"
            })
        data = PatientsStatus.objects.filter(Patient=patient).order_by('-Time')
        paginator = Paginator(data, 10)
        page_number = request.GET.get('page')
        page_data = paginator.get_page(page_number)
        return render(request, "healthtracker/patientprofile.html", {
            "data": page_data
        })
    else:
        return render(request, "healthtracker/chekhealth.html")



def addpatient(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        gender = request.POST['gender']
        roomnumber = request.POST['rnumber']
        state = request.POST['state']
        streeadd = request.POST['streetaddress']
        newpateints = Patients(
            FirstName=fname,
            LastName=lname,
            RoomNo=roomnumber,
            Gender=gender,
            Address=f"{streeadd}, {state}"
        )
        newpateints.save()
        print("new patient added")
        return render(request, "healthtracker/addpatient.html", {
            "message": "patient Added"
        })
    else:
        return render(request, "healthtracker/addpatient.html")


def addpateintdata(request):
    if request.method == 'POST':
        regnumber = request.POST['regnumber']
        pulserate = request.POST['pulserate']
        temperature = request.POST['temperature']
        try:
            patient = Patients.objects.get(RegNumber=regnumber)
        except Patients.DoesNotExist:
            patient = None
        if patient == None:
            return render(request, "healthtracker/adddata.html", {
                "message": "Registration number not found"
            })
        data = PatientsStatus(Patient=patient, PulseRate=pulserate, Temperature=temperature)
        data.save()
        print(f"Status Updated of {patient.FirstName}")
        return render(request, "healthtracker/adddata.html", {
            "message": f"Status updated!"
        })
    else:
        return render(request, "healthtracker/adddata.html")

@csrf_exempt
def pateintsdataapi(request):
    if request.method == 'GET':
        patients = Patients.objects.all()
        return JsonResponse([patient.serialize() for patient in patients], safe=False)
    if request.method == 'POST':
        data = json.loads(request.body)
        fname = data.get("fname")
        lname = data.get("lname")
        roomnumber = data.get("rnumber")
        gender = data.get("gender")
        state = data.get("state")
        streetaddress = data.get("streetaddress")
        newentry = Patients(
            FirstName=fname,
            LastName=lname,
            RoomNo=roomnumber,
            Gender=gender,
            Address=f"{streetaddress}, {state}"
        )
        newentry.save()
        return JsonResponse({"message": "Patient Added!"})


@csrf_exempt
def patientsstatusapi(request, regnumber):
    if request.method == 'GET':
        try:
            patient = Patients.objects.get(RegNumber=regnumber)
        except Patients.DoesNotExist:
            return JsonResponse({"message": "Registration number invalid!"})
        status = PatientsStatus.objects.filter(Patient=patient).order_by('-Time')
        return JsonResponse([stat.serialize() for stat in status], safe=False)
    if request.method == 'POST':
        data = json.loads(request.body)
        pulserate = data.get("pulserate")
        temp = data.get("temperature")
        try:
            patient = Patients.objects.get(RegNumber=regnumber)
        except Patients.DoesNotExist:
            return JsonResponse({"message": "Registartion Number invalid!"})
        patientdata = PatientsStatus(Patient=patient, PulseRate=pulserate, Temperature=temp)
        patientdata.save()
        return JsonResponse({"message": "Data Updated!"})
