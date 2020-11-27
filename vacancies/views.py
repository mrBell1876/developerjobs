from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render
from django.views import View

from vacancies.models import Specialty, Company


def custom_handler404(request, exception):
    return HttpResponseNotFound(' Ой, страницы не существует... Простите извините!')


def custom_handler500(request, *args, **argv):
    return HttpResponseServerError('Ой, ошибка сервера... Простите извините!')


class MainView(View):
    template_name = 'index.html'

    def get(self, request):
        all_speciality = Specialty.objects.all()
        all_company = Company.objects.all()
        context = {
            "all_speciality": all_speciality,
            "all_company": all_company
        }

        return render(request, self.template_name, context)


class CompanyView(View):
    template_name = 'company.html'

    def get(self, request, id_company):

        return render(request, self.template_name)


class VacanciesAllView(View):
    template_name = 'vacancies.html'

    def get(self, request):

        return render(request, self.template_name)


class VacanciesSpecialView(View):
    template_name = 'vacancies_cat.html'

    def get(self, request, specialisation):

        return render(request, self.template_name)


class VacancyView(View):
    template_name = 'vacancy.html'

    def get(self, request, id_vacancy):

        return render(request, self.template_name)
