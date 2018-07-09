from datetime import datetime, timedelta

import pytz
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from manger.models import Baby, Journal


class APIBabyTests(APITestCase):
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
        response = self.client.post(APIBabyTests.URL_BABY_LIST, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Baby.objects.count(), 0)

        # Проверка, какие поля необходимо заполнить
        self.assertSetEqual(set(self.BABY_MINIMUM_PARAMS), set(response.json()))

    def test_create_with_minimum_params(self):
        response = self.client.post(APIBabyTests.URL_BABY_LIST, self.BABY_MINIMUM_PARAMS)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Baby.objects.count(), 1)

        baby = Baby.objects.first()
        self.assertEqual(baby.name, self.BABY_MINIMUM_PARAMS['name'])
        self.assertEqual(baby.gender, self.BABY_MINIMUM_PARAMS['gender'])
        self.assertEqual(str(baby.birthday), self.BABY_MINIMUM_PARAMS['birthday'])

    def test_create_with_maximum_params(self):
        params = {**self.BABY_MINIMUM_PARAMS, **self.BABY_EXTRA_PARAMS}
        response = self.client.post(APIBabyTests.URL_BABY_LIST, params)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Baby.objects.count(), 1)

        baby = Baby.objects.first()
        self.assertEqual(baby.photo, self.BABY_EXTRA_PARAMS['photo'])
        self.assertEqual(baby.grade, self.BABY_EXTRA_PARAMS['grade'])
        self.assertEqual(baby.is_study, self.BABY_EXTRA_PARAMS['is_study'])

    def test_update(self):
        baby = self.createBaby()
        url_baby_detail = reverse('baby-detail', kwargs={'pk': baby.pk})

        update_pararms = {
            'name': 'new_name',
            'birthday': '1999-12-31',
            'gender': Baby.GENDER_MALE,
            'photo': '/new/path/to/image.jpeg',
            'grade': 2,
            'is_study': True,
        }
        response = self.client.put(url_baby_detail, update_pararms)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Baby.objects.count(), 1)

        baby.refresh_from_db()
        self.assertEqual(baby.name, update_pararms['name'])
        self.assertEqual(baby.gender, update_pararms['gender'])
        self.assertEqual(str(baby.birthday), update_pararms['birthday'])
        self.assertEqual(baby.photo, update_pararms['photo'])
        self.assertEqual(baby.grade, update_pararms['grade'])
        self.assertEqual(baby.is_study, update_pararms['is_study'])


class APIJournalTests(APITestCase):
    URL_JOURNAL_LIST = reverse('journal-list')

    def setUp(self):
        self.baby = Baby.objects.create(name='Петр', gender=Baby.GENDER_MALE, birthday='2010-10-01')
        self.JOURNAL_MINIMUM_PARAMS = {
            'baby': self.baby.id,
        }

        # income 2010/02/01 08:20:15
        self.income_time = datetime(2010, 2, 1, 8, 20, 15, tzinfo=pytz.utc)
        self.JOURNAL_INCOME_PARAMS = {
            'income_time': str(self.income_time),
            'income_escort': Journal.ESCORT_FATHER,
        }

        # income
        self.outcome_time = self.income_time + timedelta(hours=8)
        self.JOURNAL_OUTCOME_PARAMS = {
            'outcome_time': str(self.outcome_time),
            'outcome_escort': Journal.ESCORT_MOTHER,
        }

    def createEmptyRecord(self):
        return Journal.objects.create(baby=self.baby)

    def test_create_with_empty_params(self):
        response = self.client.post(APIJournalTests.URL_JOURNAL_LIST, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Journal.objects.count(), 0)

        # Проверка, какие поля необходимо заполнить
        self.assertSetEqual(set(self.JOURNAL_MINIMUM_PARAMS), set(response.json()))

    def test_create_without_income_and_outcome(self):
        response = self.client.post(APIJournalTests.URL_JOURNAL_LIST, self.JOURNAL_MINIMUM_PARAMS)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Journal.objects.count(), 1)

        record = Journal.objects.first()
        self.assertEqual(record.baby, self.baby)
        self.assertIsNone(record.income_time)
        self.assertIsNone(record.income_escort)
        self.assertIsNone(record.outcome_time)
        self.assertIsNone(record.outcome_escort)

    def test_create_with_income(self):
        params = {**self.JOURNAL_MINIMUM_PARAMS, **self.JOURNAL_INCOME_PARAMS}
        response = self.client.post(APIJournalTests.URL_JOURNAL_LIST, params)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Journal.objects.count(), 1)

        record = Journal.objects.first()
        self.assertEqual(record.baby, self.baby)
        self.assertEqual(record.income_time, self.income_time)
        self.assertEqual(record.income_escort, self.JOURNAL_INCOME_PARAMS['income_escort'])

    def test_create_with_income_incorrect(self):
        # удаляем информацию о сопровождающе
        del self.JOURNAL_INCOME_PARAMS['income_escort']
        params = {**self.JOURNAL_MINIMUM_PARAMS, **self.JOURNAL_INCOME_PARAMS}
        response = self.client.post(APIJournalTests.URL_JOURNAL_LIST, params)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_with_outcome(self):
        # нельзя создать outcome без income
        params = {**self.JOURNAL_MINIMUM_PARAMS, **self.JOURNAL_OUTCOME_PARAMS}
        response = self.client.post(APIJournalTests.URL_JOURNAL_LIST, params)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_with_income_and_outcome_correct(self):
        params = {**self.JOURNAL_MINIMUM_PARAMS, **self.JOURNAL_INCOME_PARAMS, **self.JOURNAL_OUTCOME_PARAMS}
        response = self.client.post(APIJournalTests.URL_JOURNAL_LIST, params)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Journal.objects.count(), 1)

        record = Journal.objects.first()
        self.assertEqual(record.baby, self.baby)
        self.assertEqual(record.income_time, self.income_time)
        self.assertEqual(record.income_escort, self.JOURNAL_INCOME_PARAMS['income_escort'])
        self.assertEqual(record.outcome_time, self.outcome_time)
        self.assertEqual(record.outcome_escort, self.JOURNAL_OUTCOME_PARAMS['outcome_escort'])

    def test_create_with_outcome_early_that_income(self):
        self.outcome_time = self.income_time - timedelta(hours=3)
        self.JOURNAL_OUTCOME_PARAMS['outcome_time'] = str(self.outcome_time)
        params = {**self.JOURNAL_MINIMUM_PARAMS, **self.JOURNAL_INCOME_PARAMS, **self.JOURNAL_OUTCOME_PARAMS}
        response = self.client.post(APIJournalTests.URL_JOURNAL_LIST, params)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Journal.objects.count(), 0)

    def test_update_with_income(self):
        record = self.createEmptyRecord()
        url_journal_detail = reverse('journal-detail', kwargs={'pk': record.pk})

        params = {**self.JOURNAL_MINIMUM_PARAMS, **self.JOURNAL_INCOME_PARAMS}
        response = self.client.put(url_journal_detail, params)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Journal.objects.count(), 1)

        record.refresh_from_db()
        self.assertEqual(record.income_time, self.income_time)
        self.assertEqual(record.income_escort, self.JOURNAL_INCOME_PARAMS['income_escort'])

    def test_update_with_outcome_without_income(self):
        record = self.createEmptyRecord()
        url_journal_detail = reverse('journal-detail', kwargs={'pk': record.pk})

        params = {**self.JOURNAL_MINIMUM_PARAMS, **self.JOURNAL_OUTCOME_PARAMS}
        response = self.client.put(url_journal_detail, params)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Journal.objects.count(), 1)

        record.refresh_from_db()
        self.assertIsNone(record.outcome_time)
        self.assertIsNone(record.outcome_escort)
        
    def test_baby_study_list(self):
        b1 = Baby.objects.create(name='Name1', gender=Baby.GENDER_MALE, birthday='2000-01-01', grade=1, is_study=True)
        b2 = Baby.objects.create(name='Name2', gender=Baby.GENDER_MALE, birthday='2000-01-02', grade=2, is_study=False)
        b3 = Baby.objects.create(name='Name3', gender=Baby.GENDER_MALE, birthday='2000-01-03', grade=3, is_study=True)
        b4 = Baby.objects.create(name='Name4', gender=Baby.GENDER_MALE, birthday='2000-01-04', grade=4, is_study=False)

        j1_1, j1_2 = Journal.objects.create(baby=b1), Journal.objects.create(baby=b1)
        Journal.objects.create(baby=b2), Journal.objects.create(baby=b2)
        j3 = Journal.objects.create(baby=b3)
        Journal.objects.create(baby=b4)

        response = self.client.get(reverse('journal-study'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertSetEqual({j1_1.id, j1_2.id, j3.id}, set([record['id'] for record in response.json()]))
