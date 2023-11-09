import json

from django.test import TestCase, Client

from .models import Patient, Doctor, Opening_hour, No_covered

url = 'api/v1/accounts/'


class PatientTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Patient.objects.create(name="창희")

    def test_create_success(self):
        patient = Patient.objects.get(name="창희").name
        self.assertEqual(patient, "창희")


class DoctorTest(TestCase):
    def test_create_doctor(self):
        client = Client()

        doctor = {
            "name": "김민지",
            "hospital": "민수가정의원",
            "department": "가정의학과, 소아과, 피부과",
            "no_covered": [{
                "subject": "다이어트약"
            }],
            "time": [{
                "day": 0,
                "work": 1,
                "lunch": 1,
                "start": "0900",
                "end": "1800",
                "lunch_start": "1200",
                "lunch_end": "1300"
            }, {
                "day": 1,
                "work": 1,
                "lunch": 1,
                "start": "0900",
                "end": "1800",
                "lunch_start": "1200",
                "lunch_end": "1300"
            }, {
                "day": 2,
                "work": 1,
                "lunch": 1,
                "start": "0900",
                "end": "1800",
                "lunch_start": "1200",
                "lunch_end": "1300"
            }, {
                "day": 3,
                "work": 1,
                "lunch": 1,
                "start": "0900",
                "end": "1900",
                "lunch_start": "1200",
                "lunch_end": "1300"
            }, {
                "day": 4,
                "work": 1,
                "lunch": 1,
                "start": "0900",
                "end": "1800",
                "lunch_start": "1200",
                "lunch_end": "1300"
            }, {
                "day": 5,
                "work": 1,
                "lunch": 0,
                "start": "0900",
                "end": "1800",
                "lunch_start": "0000",
                "lunch_end": "0000"
            }, {
                "day": 6,
                "work": 0,
                "lunch": 0,
                "start": "0000",
                "end": "0000",
                "lunch_start": "0000",
                "lunch_end": "0000"
            }]
        }

        response = client.post(
            url + 'create/doctor/', json.dumps(doctor), content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)

    def test_wrong_time_type(self):
        client = Client()
        doctor = {
            "name": "김민지",
            "hospital": "민수가정의원",
            "department": "가정의학과, 소아과, 피부과",
            "no_covered": [{
                "subject": "다이어트약"
            }],
            "time": [{
                "day": 0,
                "work": 1,
                "lunch": 1,
                "start": "0900",
                "end": "1800",
                "lunch_start": "1200",
                "lunch_end": "1300"
            }, {
                "day": 1,
                "work": 1,
                "lunch": 1,
                "start": "0900",
                "end": "1800",
                "lunch_start": "1200",
                "lunch_end": "1300"
            }, {
                "day": 2,
                "work": 1,
                "lunch": 1,
                "start": "0900",
                "end": "1800",
                "lunch_start": "1200",
                "lunch_end": "1300"
            }, {
                "day": 3,
                "work": 1,
                "lunch": 1,
                "start": "0900",
                "end": "1900",
                "lunch_start": "1200",
                "lunch_end": "1300"
            }, {
                "day": 4,
                "work": 1,
                "lunch": 1,
                "start": "0900",
                "end": "1800",
                "lunch_start": "1200",
                "lunch_end": "1300"
            }, {
                "day": 5,
                "work": 1,
                "lunch": 0,
                "start": "0900",
                "end": "1800",
                "lunch_start": "0000",
                "lunch_end": "0000"
            }, {
                "day": 6,
                "work": 0,
                "lunch": 0,
                "start": "0000",
                "end": "0000",
                "lunch_start": "0000",
                "lunch_end": "0000"
            }]
        }

        response = client.post(
            url + 'create/doctor/', json.dumps(doctor), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"data": "영업시간이 올바른 형식이 아닙니다"})

    def test_serach_word(self):
        client = Client()

        data = {
            "type": "string",
            "detail": "정수내과의원 박정수"
        }

        response = client.get(
            url + 'search/', data=data
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"name": "박정수"}])

    def test_search_datetime(self):
        client = Client()

        data = {
            "type": "datetime",
            "detail": "202303201010"
        }

        response = client.get(
            url + 'search/', data=data
        )

        self.assertEqual(response.json(), [{"name": "박정수"}, {"name": "박정민"}])
