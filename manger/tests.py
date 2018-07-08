from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from manger.models import Baby


class BabyTests(APITestCase):
    URL_BABY_LIST = reverse('baby-list')

    def setUp(self):
        self.BABY_MINIMUM_PARAMS = {
            'name': 'Иван',
            'gender': Baby.GENDER_MALE,
            'birthday': '2000-01-01',
        }
        self.BABY_EXTRA_PARAMS = {
            'photo': '/path/to/image.jpeg',
            'grade': 3,
            'is_study': False,
        }

    def createBaby(self):
        return Baby.objects.create(**self.BABY_MINIMUM_PARAMS)

    def test_create_with_empty_params(self):
        response = self.client.post(BabyTests.URL_BABY_LIST, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Baby.objects.count(), 0)

        # Проверка, какие поля необходимо заполнить
        self.assertSetEqual(set(self.BABY_MINIMUM_PARAMS), set(response.json()))

    def test_create_with_minimum_params(self):
        response = self.client.post(BabyTests.URL_BABY_LIST, self.BABY_MINIMUM_PARAMS, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Baby.objects.count(), 1)

        baby = Baby.objects.first()
        self.assertEqual(baby.name, self.BABY_MINIMUM_PARAMS['name'])
        self.assertEqual(baby.gender, self.BABY_MINIMUM_PARAMS['gender'])
        self.assertEqual(str(baby.birthday), self.BABY_MINIMUM_PARAMS['birthday'])

    def test_create_with_maximum_params(self):
        params = {**self.BABY_MINIMUM_PARAMS, **self.BABY_EXTRA_PARAMS}
        response = self.client.post(BabyTests.URL_BABY_LIST, params, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Baby.objects.count(), 1)

        baby = Baby.objects.first()
        self.assertEqual(baby.photo, self.BABY_EXTRA_PARAMS['photo'])
        self.assertEqual(baby.grade, self.BABY_EXTRA_PARAMS['grade'])
        self.assertEqual(baby.is_study, self.BABY_EXTRA_PARAMS['is_study'])

    def test_update(self):
        baby = self.createBaby()
        URL_BABY_DETAIL = reverse('baby-detail', kwargs={'pk': baby.pk})

        update_pararms = {
            'name': 'new_name',
            'birthday': '1999-12-31',
            'gender': Baby.GENDER_MALE,
            'photo': '/new/path/to/image.jpeg',
            'grade': 2,
            'is_study': True,
        }
        response = self.client.put(URL_BABY_DETAIL, update_pararms, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Baby.objects.count(), 1)

        baby.refresh_from_db()
        self.assertEqual(baby.name, update_pararms['name'])
        self.assertEqual(baby.gender, update_pararms['gender'])
        self.assertEqual(str(baby.birthday), update_pararms['birthday'])
        self.assertEqual(baby.photo, update_pararms['photo'])
        self.assertEqual(baby.grade, update_pararms['grade'])
        self.assertEqual(baby.is_study, update_pararms['is_study'])
