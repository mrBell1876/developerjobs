from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from django.shortcuts import render
from django.views import View

from vacancies.models import Specialty, Company, Vacancy


def custom_handler404(request, *args, **argv):
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
        if not Company.objects.filter(id__iexact=id_company):
            raise Http404
        company = Company.objects.get(id=id_company)
        company_vacancies = Vacancy.objects.filter(company__id=id_company)
        context = {
            "company_vacancies": company_vacancies,
            "company": company
        }
        return render(request, self.template_name, context)


class VacanciesAllView(View):
    template_name = 'vacancies.html'

    def get(self, request):
        all_vacancy = Vacancy.objects.all()
        context = {
            "all_vacancy": all_vacancy,
        }
        return render(request, self.template_name, context)


class VacanciesSpecialView(View):
    template_name = 'vacancies_cat.html'

    def get(self, request, specialisation):
        if not Specialty.objects.filter(code__iexact=specialisation):
            raise Http404
        category = Specialty.objects.get(code=specialisation)
        cat_vacancies = Vacancy.objects.filter(specialty__code=specialisation)
        context = {
            "cat_vacancies": cat_vacancies,
            "category": category
        }
        return render(request, self.template_name, context)


class VacancyView(View):
    template_name = 'vacancy.html'

    def get(self, request, id_vacancy):
        if not Vacancy.objects.filter(id__iexact=id_vacancy):
            raise Http404
        vacancy = Vacancy.objects.get(id=id_vacancy)
        context = {
            "vacancy": vacancy
        }
        return render(request, self.template_name, context)
