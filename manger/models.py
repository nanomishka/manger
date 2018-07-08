from django.db import models


class Baby(models.Model):
    GENDER_MALE = 1
    GENDER_FEMALE = 0

    GENDER_CHOICES = (
        (GENDER_MALE, 'мальчик'),
        (GENDER_FEMALE, 'девочка'),
    )

    name = models.CharField('Имя', max_length=50, blank=False)
    gender = models.SmallIntegerField('Пол', choices=GENDER_CHOICES)
    birthday = models.DateField('Дата рождения')
    photo = models.CharField('Фото', max_length=100)
    grade = models.SmallIntegerField('Класс', null=True)
    is_study = models.BooleanField('Учится?')

    def __str__(self):
        return '%s [%s]' % (self.name, self.birthday)


class Journal(models.Model):
    ESCORT_FATHER = 0
    ESCORT_MOTHER = 1

    ESCORT_CHOICES = (
        (ESCORT_FATHER, 'отец'),
        (ESCORT_MOTHER, 'мать'),
    )

    baby = models.ForeignKey(Baby, verbose_name='Ребенок', on_delete=models.CASCADE)

    # income
    income_time = models.DateTimeField('Время прибытия', null=True)
    income_escort = models.SmallIntegerField('Сопровождающее лицо', choices=ESCORT_CHOICES, null=True)

    # outcome
    outcome_time = models.DateTimeField('Время прибытия', null=True)
    outcome_escort = models.SmallIntegerField('Сопровождающее лицо', choices=ESCORT_CHOICES, null=True)

    def __str__(self):
        return '%s: %s - %s ' % (self.baby, self.income_time or '***', self.outcome_time or '***')
