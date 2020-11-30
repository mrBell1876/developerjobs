from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from developerjobs.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR


class Company(models.Model):
    name = models.CharField(max_length=70)
    location = models.CharField(max_length=70)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR, height_field='height_field',
                             width_field='width_field')
    height_field = 100
    width_field = 60
    description = models.TextField()
    employee_count = models.IntegerField()
    owner = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='company')


class Specialty(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=70)
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR, height_field='height_field',
                                width_field='width_field')
    height_field = 80
    width_field = 80


class Vacancy(models.Model):
    title = models.CharField(max_length=70)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.TextField()
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()


class Application(models.Model):
    written_username = models.CharField(max_length=20)
    written_phone = models.IntegerField()
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
