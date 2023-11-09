from django.test import TestCase, Client

# Create your tests here.

url = 'api/v1/diagnosis/'


class DiagnosisTest(TestCase):
    def test_create_diagnosis(self):
        client = Client()

        data = {
            "patient": 1,
            "doctor": 3,
            "datetime": "202311141400"
        }

        response = client.post(
            url + 'request/', data=data, content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)

    def test_diagnosis_not_work_time(self):
        client = Client()

        data = {
            "patient": 1,
            "doctor": 3,
            "datetime": "202311141200"
        }

        response = client.post(
            url + 'request/', data=data, content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"data": "병원 진료시간이 아닙니다"
        })

    def test_diagnosis_wrong_time_type(self):
        data = {
            "patient": 1,
            "doctor": 6,
            "datetime": "간다나라"
        }

        response = Client().post(
            url + 'request/', data = data, content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"data": "잘못된 시간형식입니다"})
    
    def test_diagnosis_before_now(self):
        data = {
            "patient": 1,
            "doctor": 6,
            "datetime": "20221103201110"
        }

        response = Client().post(
            url + 'request/', data = data, content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"data": "잘못된 시간형식입니다"})

    def test_diagnosis_not_work_time(self):
        data = {
            "patient": 1,
            "doctor": 6,
            "datetime": "202311151300"
        }

        response = Client().post(
            url + 'request/', data = data, content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"data": "병원 진료시간이 아닙니다"})

    def test_diagnosis_search(self):
        data = {
            "doctor": 5,
        }

        response = Client().get(
            url + 'search/', data=data
        )

        self.assertEqual(len(response.json()), 1)
    
    def test_accepted_diagnosis(self):
        data = {
            "diagnosis": 4,
        }

        response = Client().put(
            url + 'accepted/', data=data
        )

        self.assertEqual(response.json().get("accepted"), True)