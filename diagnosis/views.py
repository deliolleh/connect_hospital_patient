import calendar

from datetime import datetime, date

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from accounts.models import Patient, Doctor, Opening_hour
from .models import Diagnosis
from .serializers import DiagnosisCreatedSerializer, DiagnosisShowSerializer, DiagnosisSerializer


def check_day_vaildation(year, month, day, hour, minute):
    try:
        datetime(year, month, day, hour, minute)
    except:
        return False
    return True


def change_datetime(y, m, d, h, mi):
    year, month, day, hour, minute = y, m, d, h, mi
    if minute >= 60:
        minute -= 60
        hour += 1

        if hour >= 24:
            hour -= 24
            day += 1

            day_of_month = calendar.monthrange(year, month)
            if day_of_month < day:
                day -= day_of_month
                month += 1

                if month > 12:
                    year += 1
                    month -= 12
    return year, month, day, hour, minute


def change_date(day_of_week, timeline):
    # 정상적인 경우 1주일 내에 진료시간이 있어야하기 때문에 무한루프를 방지하고자 while의 범위 설정
    next_time = 0
    i = 1

    while i < 7:
        next_day = (day_of_week + i) % 7
        next_time = timeline.get(day=next_day)
        if next_time.work:
            return i
        i += 1
    else:
        return False


# 진료 요청
@api_view(["POST"])
def requet_diagnosis(request):
    # input
    patient_id = request.data.get("patient")
    doctor_id = request.data.get("doctor")
    date_time = request.data.get("datetime")

    # wanted day
    year, month, day, hour, minute = \
    date_time[0:4], date_time[4:6], date_time[6:8], date_time[8:10], date_time[10:]

    try:
        year, month, day, hour, minute = int(year), int(month), int(day), int(hour), int(minute)
        
    except ValueError:
        return JsonResponse({"data": "잘못된 시간형식입니다"}, status=400)
        

    if not check_day_vaildation(year, month, day, int(hour), int(minute)) or\
        datetime(year, month,day) < datetime.now():
        return JsonResponse({"data": "오늘보다 이전의 시간은 예약할 수 없습니다"}, status=400)

    day_of_week = date(year=year, month=month, day=day).weekday()

    # call foreign key
    patient = get_object_or_404(Patient, pk=patient_id)
    doctor = get_object_or_404(Doctor, pk=doctor_id)

    # call wanted day of week schedule
    open_times = Opening_hour.objects.filter(doctor=doctor)
    open_time = open_times.get(day=day_of_week)
    hour_minute = hour * 100 + minute
    start = int(open_time.start)
    end = int(open_time.end)
    start_l = int(open_time.lunch_start)
    end_l = int(open_time.lunch_end)

    # check wanted day
    data = dict()
    data["accepted"] = False
    if open_time.work and open_time.lunch and (start <= hour_minute < start_l or end_l < hour_minute <= end):
        data["wanted_time"] = datetime(year, month, day, int(hour), int(minute))

        # now datetime for expired time
        now = datetime.now()
        now_year, now_month, now_day, now_hour, now_minute = int(now.strftime("%Y")), int(now.strftime("%m")), int(
            now.strftime("%d")), now.strftime("%H"), now.strftime("%M")
        hour_minute2 = int(now_hour + now_minute)

        today_of_week = date(now_year, now_month, now_day).weekday()
        open_time2 = open_times.get(day=today_of_week)

        start2 = int(open_time2.start)
        start_l2 = int(open_time2.lunch_start)
        end_l2 = int(open_time2.lunch_end)
        end2 = int(open_time2.end)

        next_time = 0

        if open_time2.work:
            if (open_time2.lunch and (start2 <= hour_minute2 < start_l2 or end_l2 < hour_minute2 <= end2)) or (
                    not open_time2.lunch and (start2 <= hour_minute2 <= end2)):
                y, m, d, h, mi = change_datetime(now_year, now_month, now_day, int(now_hour), int(now_minute) + 20)
                data["expired_time"] = datetime(y, m, d, h, mi)

            elif open_time2.lunch and start_l2 <= hour_minute2 <= end_l2:
                data["expired_time"] = datetime(now_year, now_month, now_day, int(str(end_l2)[0:2]),
                                                int(str(end_l2)[2:]) + 15)

            elif hour_minute2 < start2:
                data["expired_time"] = datetime(now_year, now_month, now_day, int(str(start2)[0:2]), int(str(start2)[2:]) + 15)

            elif end2 < hour_minute2:
                next_time = 1

        else:
            next_time = 1

        if next_time:
            term_day = change_date(today_of_week, open_times)
            if term_day:
                open_time3 = open_times.get(day=(today_of_week + term_day) % 7)
                now_day += term_day
                this_month = calendar.monthrange(now_year, now_month)
                if this_month < now_day:
                    now_day -= this_month
                    now_month += 1
                    if now_month > 12:
                        now_month -= 12
                        now_year += 1

                data["expired_time"] = datetime(now_year, now_month, now_day, int(open_time3.start[0:2]),int(open_time3.start[2:]))

            else:
                return JsonResponse({"data": "서버에 오류가 발생했습니다"}, status=508)

        serializer = DiagnosisCreatedSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(doctor=doctor, patient=patient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


    else:
        return JsonResponse({"data": "병원 진료시간이 아닙니다"}, status=400)


# 진료요청 검색
@api_view(["GET"])
def search_diagnosis(request):
    doctor = request.data.get("doctor")

    diagnosises = Diagnosis.objects.filter(doctor=doctor, accepted=False)
    serializer = DiagnosisShowSerializer(diagnosises, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# 진료요청 수락
@api_view(["PUT"])
def accepted_diagnosis(request):
    pk = request.data.get("diagnosis")

    # 이미 승인한 진료 요청은 가져오기 않도록
    diagnosis = get_object_or_404(Diagnosis.objects.all(), pk=pk, accepted=False)
    data = {
        "pk": diagnosis.pk,
        "patient": diagnosis.patient.pk,
        "doctor": diagnosis.doctor.pk,
        "accepted": True,
        "wanted_time": diagnosis.wanted_time,
        "expired_time": diagnosis.expired_time
    }
    serializer = DiagnosisSerializer(instance=diagnosis, data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
