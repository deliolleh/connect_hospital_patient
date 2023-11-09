from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.requet_diagnosis),
    path('search/', views.search_diagnosis),
    path('accepted/', views.accepted_diagnosis)
]
