from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from vacancies.forms import SearchForm, ApplicationForm
from vacancies.models import Specialty, Company, Vacancy, Application


def custom_handler404(request, *args, **argv):
    return HttpResponseNotFound(' Ой, страницы не существует... Простите извините!')


def custom_handler500(request, *args, **argv):
    return HttpResponseServerError('Ой, ошибка сервера... Простите извините!')


class MainView(View):
    template_name = 'index.html'
    form_search = SearchForm()

    def get(self, request):
        all_speciality = Specialty.objects.all()
        all_company = Company.objects.all()
        context = {
            "all_speciality": all_speciality,
            "all_company": all_company,
            "form": self.form_search
        }

        return render(request, self.template_name, context)


class Search(View):
    template_name = 'search.html'

    def get(self, request, **argv):
        search_form = SearchForm
        context = {'form': search_form}
        query = self.request.GET.get('find')
        if query is not None:
            vacancy_list = Vacancy.objects.filter(
                Q(title__icontains=query) | Q(skills__icontains=query) | Q(description__icontains=query)
            )
            context = {
                'vacancy_list': vacancy_list,
                'form': SearchForm(request.GET)
            }
            return render(request, self.template_name, context)

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
    search_form = SearchForm

    def get(self, request):
        all_vacancy = Vacancy.objects.all()
        context = {
            "all_vacancy": all_vacancy,
            'form': self.search_form
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
    form_class = ApplicationForm
    success_url = 'send/'

    def get(self, request, id_vacancy):
        if not Vacancy.objects.filter(id__iexact=id_vacancy):
            raise Http404
        vacancy = Vacancy.objects.get(id=id_vacancy)
        context = {
            "vacancy": vacancy,
            "form": self.form_class
        }
        return render(request, self.template_name, context)

    def post(self, request, id_vacancy):
        form_class = ApplicationForm(request.POST)
        if form_class.is_valid():
            data = form_class.cleaned_data
            add_application = Application.objects.create(
                written_username=data["name"],
                written_phone=data["phone"],
                written_cover_letter=data["message"],
                vacancy=Vacancy.objects.get(id=id_vacancy),
                user=request.user if request.user.is_authenticated else None,
            )
            return HttpResponseRedirect(self.success_url)
        else:
            vacancy = Vacancy.objects.get(id=id_vacancy)
            context = {
                "vacancy": vacancy,
                "form": form_class
            }
            return render(request, self.template_name, context)


class SendApplicationView(View):
    template_name = 'sent.html'

    def get(self, request, **argv):
        return render(request, self.template_name)