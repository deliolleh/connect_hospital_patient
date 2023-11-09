from datetime import datetime

from django.db.models import Q
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Doctor, Patient, No_covered
from .serializers.created import PatientCreateSerializer, DoctorCreateSerializer, Opening_HourCreatedSerializer, \
    No_coverCreatedSerializer, DoctorCreateShowSerializer
from .serializers.response import DoctorShowSerializer


# View

# 일반 회원 등록
@api_view(["POST"])
def regist_patient(request):
    serializer = PatientCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True) and not Patient.objects.filter(name=request.data.get("name")):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 의사 회원 등록
@api_view(["POST"])
def regist_doctor(request):
    name = request.data.get("name")
    hospital = request.data.get("hospital")
    no_covereds = request.data.get("no_covered")
    times = request.data.get("time")
    for check_time in times:
        if (not check_time.get("start").isdecimal() or not check_time.get("end").isdecimal() or
                not check_time.get("lunch_start").isdecimal() or not check_time.get("lunch_end").isdecimal()):
            return JsonResponse({"data": "영업시간이 올바른 형식이 아닙니다"}, status=400)

    # serializer1 = DoctorCreateSerializer(name = name, hospital = hospital, department = department)
    serializer1 = DoctorCreateSerializer(data=request.data)
    if serializer1.is_valid(raise_exception=True) and not Doctor.objects.filter(name=name, hospital=hospital):
        serializer1.save()
        target = Doctor.objects.get(name=name, hospital=hospital)
        for no_covered in no_covereds:
            serializer2 = No_coverCreatedSerializer(data=no_covered)
            if serializer2.is_valid(raise_exception=True):
                serializer2.save(doctor=target)
            else:
                target.delete()
        for time in times:
            serializer3 = Opening_HourCreatedSerializer(data=time)
            if serializer3.is_valid(raise_exception=True):
                serializer3.save(doctor=target)
            else:
                No_covered.objects.filter(doctor=target).delete()
                target.delete()
        serializer = DoctorCreateShowSerializer(target)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    else:
        return JsonResponse({"data": "올바른 형식이 아닙니다"}, status=400)


# 의사 검색
@api_view(["GET"])
def search_doctor(request):
    classify = request.data.get("type")
    detail = request.data.get("detail")
    if classify == "string":
        words = detail.split()
        doctors = Doctor.objects
        for word in words:
            doctors = doctors.filter(Q(name__contains=word) | Q(hospital__contains=word) | Q(department__contains=word))
        serializer = DoctorShowSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        year = int(detail[0:4])
        month = int(detail[4:6])
        day = int(detail[6:8])
        hour_minute = detail[8:]

        day_of_week = datetime(year, month, day).weekday()

        base = Doctor.objects
        part1 = base.filter(opentimes__day=day_of_week, opentimes__work=1)
        part2 = part1.filter(opentimes__lunch=1, opentimes__start__lte=hour_minute,
                            opentimes__lunch_start__gt=hour_minute)
        part3 = part1.filter(opentimes__lunch=1, opentimes__lunch_end__lte=hour_minute, opentimes__end__gt=hour_minute)
        part4 = part1.filter(opentimes__lunch=0, opentimes__start__lte=hour_minute, opentimes__end__gt=hour_minute)

        doctors = part2.union(part3, part4)

        serializer = DoctorShowSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
