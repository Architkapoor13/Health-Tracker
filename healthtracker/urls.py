from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("adminlogin", views.login_view, name="admin-login"),
    path("logout", views.logout_view, name="logout"),
    path("checkhealth", views.checkhealth, name="checkhealth"),
    path("addpatient", views.addpatient, name="addpatient"),
    path("addpatientdata", views.addpateintdata, name="adddata"),

    # API urls
    path("patientsdataapi", views.pateintsdataapi, name="pdataapi"),
    path("patientsstatusapi/<str:regnumber>", views.patientsstatusapi, name="pstatusapi")
]