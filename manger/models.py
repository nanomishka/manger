from django.db import models


class Baby(models.Model):
    GENDER_MALE = 0
    GENDER_FEMALE = 1

    GENDER_CHOICES = (
        (GENDER_MALE, 'мальчик'),
        (GENDER_FEMALE, 'девочка'),
    )

    MAX_LENGTH_NAME = 50
    MAX_LENGTH_PHOTO = 100

    # required
    name = models.CharField('Имя', max_length=MAX_LENGTH_NAME, blank=False)
    gender = models.SmallIntegerField('Пол', choices=GENDER_CHOICES)
    birthday = models.DateField('Дата рождения')

    photo = models.CharField('Фото', max_length=MAX_LENGTH_PHOTO, blank=True)
    grade = models.SmallIntegerField('Класс', null=True)
    is_study = models.BooleanField('Учится?', default=False)

    def __str__(self):
        return '%s [%s]' % (self.name, self.birthday)


class Journal(models.Model):
    ESCORT_FATHER = 0
    ESCORT_MOTHER = 1

    ESCORT_CHOICES = (
        (ESCORT_FATHER, 'отец'),
        (ESCORT_MOTHER, 'мать'),
    )

    # required
    baby = models.ForeignKey(Baby, verbose_name='Ребенок', on_delete=models.CASCADE)

    # income
    income_time = models.DateTimeField('Время прибытия', null=True)
    income_escort = models.SmallIntegerField('Сопровождающее лицо', choices=ESCORT_CHOICES, null=True)

    # outcome
    outcome_time = models.DateTimeField('Время прибытия', null=True)
    outcome_escort = models.SmallIntegerField('Сопровождающее лицо', choices=ESCORT_CHOICES, null=True)

    def __str__(self):
        return '%s: %s - %s ' % (self.baby, self.income_time or '***', self.outcome_time or '***')
