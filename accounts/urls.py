from django.urls import path
from . import views

urlpatterns = [
    path('create/patient/', views.regist_patient),
    path('create/doctor/', views.regist_doctor),
    path('search/', views.search_doctor),
]
