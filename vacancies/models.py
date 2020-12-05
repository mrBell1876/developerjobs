from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from developerjobs.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR


class Company(models.Model):
    name = models.CharField(max_length=70, verbose_name="Название компании")
    location = models.CharField(max_length=70, verbose_name="География")
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR, height_field='height_field',
                             width_field='width_field', verbose_name="Логотип")
    height_field = 100
    width_field = 60
    description = models.TextField(verbose_name="Информация о компании")
    employee_count = models.IntegerField(verbose_name="Количество человек в компании")
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')

    def __str__(self):
        return self.name


class Specialty(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=70)
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR, height_field='height_field',
                                width_field='width_field')
    height_field = 80
    width_field = 80

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    title = models.CharField(max_length=70, verbose_name='Название вакансии')
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE,
                                  verbose_name='Специализация', related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.TextField(verbose_name='Навыки')
    description = models.TextField(verbose_name='Описание вакансии')
    salary_min = models.IntegerField(verbose_name='Зарплата от')
    salary_max = models.IntegerField(verbose_name='Зарплата до')
    published_at = models.DateField()

    def __str__(self):
        return self.title


class Application(models.Model):
    written_username = models.CharField(max_length=20)
    written_phone = models.IntegerField()
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='applications')

    def __str__(self):
        return self.written_username


class Resume(models.Model):

    grade_CHOICES = (
                        ('TR', 'Стажер'),
                        ('JN', 'Джуниор'),
                        ('ML', 'Миддл'),
                        ('SN', 'Синьор'),
                        ('LD', 'Лид'))
    status_CHOISES = (
        ('busy', 'Не ищу работу'),
        ('open', 'Рассматриваю предложения'),
        ('find', 'Ищу работу')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resume')
    name = models.CharField(max_length=20, verbose_name='Имя')
    surname = models.CharField(max_length=20, verbose_name='Фамилия')
    status_CHOISES = models.CharField(max_length=100, verbose_name='Готовность к работе', choices=status_CHOISES)
    salary = models.IntegerField(verbose_name='Зарплата')
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE,
                                  verbose_name='Специализация', related_name='resume')
    grade = models.CharField(max_length=100, verbose_name='Квалификация', choices=grade_CHOICES)
    education = models.TextField(verbose_name='Образование')
    experience = models.TextField(verbose_name='Опыт работы')
    portfolio = models.URLField(max_length=200, verbose_name="ссылка на портфолио")
