from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView

from vacancies.forms import RegisterForm, LoginForm, ApplicationForm, MyCompanyEditForm, MyVacancyEditForm
from vacancies.models import Specialty, Company, Vacancy, Application


def custom_handler404(request, *args, **argv):
    return HttpResponseNotFound(' Ой, страницы не существует... Простите извините!')


def custom_handler500(request, *args, **argv):
    return HttpResponseServerError('Ой, ошибка сервера... Простите извините!')


class MySignupView(CreateView):
    form_class = RegisterForm
    success_url = '../login/'
    template_name = 'register.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form_class = RegisterForm(request.POST)
        if form_class.is_valid():
            data = form_class.cleaned_data
            User.objects.create_user(
                username=data['login'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password=data['password']
            )
            return HttpResponseRedirect(self.success_url)


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'
    form_class = LoginForm


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


class VacancyView(CreateView):
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


class MyCompanyView(View):
    template_name = 'my-company.html'

    @method_decorator(login_required)
    def get(self, request, **argv):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("letsstart/")

        if not Company.objects.filter(owner=request.user):
            return HttpResponseRedirect("letsstart/")
        else:
            company = Company.objects.get(owner=request.user)
            company_form = MyCompanyEditForm(instance=company)
            context = {
                "form": company_form
            }
            return render(request, self.template_name, context)

    def post(self, request, **argv):
        company = Company.objects.get(owner=request.user)
        company_form = MyCompanyEditForm(request.POST, request.FILES, instance=company)

        if company_form.is_valid():
            company = company_form.save(commit=False)
            company.owner = request.user
            company.save()
            context = {

                "form": company_form,
                "success_send": True
            }
            return render(request, self.template_name, context)
        else:
            context = {

                "form": company_form
            }
            return render(request, self.template_name, context)


class MyCompanyStart(View):
    template_name = 'my-company-lets-start.html'

    def get(self, request, **argv):
        return render(request, self.template_name)


class MyCompanyCreateView(View):
    template_name = 'my-company-create.html'
    form_class = MyCompanyEditForm()
    success_url = '/mycompany'

    @method_decorator(login_required)
    def get(self, request, **argv):
        if Company.objects.filter(owner=request.user):
            return HttpResponseRedirect(self.success_url)
        context = {
            "form": self.form_class
        }
        return render(request, self.template_name, context)

    def post(self, request, **argv):
        form_class = MyCompanyEditForm(request.POST, request.FILES)
        if form_class.is_valid():
            company = form_class.save(commit=False)
            company.owner = request.user
            company.save()
            return HttpResponseRedirect(self.success_url)
        else:
            context = {

                "form": form_class
            }
            return render(request, self.template_name, context)


class MyVacanciesView(View):
    template_name = 'vacancy-list.html'

    @method_decorator(login_required)
    def get(self, request, **argv):
        company_vacancies = Vacancy.objects.filter(company__id=request.user.company.id)
        context = {
            "company_vacancies": company_vacancies,
        }
        return render(request, self.template_name, context)


class EditVacancyView(View):
    template_name = 'vacancy-edit.html'

    @method_decorator(login_required)
    def get(self, request, vacancy_id, **argv):
        if not Vacancy.objects.filter(id=vacancy_id, company=request.user.company):
            return HttpResponseRedirect("/")
        else:
            vacancy = Vacancy.objects.get(id=vacancy_id)
            vacancy_form = MyVacancyEditForm(instance=vacancy)
            applications_list = Application.objects.filter(vacancy=vacancy)
            context = {
                "form": vacancy_form,
                "vacancy": vacancy,
                "applications_list": applications_list,
            }
            return render(request, self.template_name, context)

    def post(self, request, vacancy_id, **argv):
        select_vacancy = Vacancy.objects.get(id=vacancy_id)
        vacancy_form = MyVacancyEditForm(request.POST, instance=select_vacancy)

        if vacancy_form.is_valid():
            vacancy = vacancy_form.save(commit=False)
            vacancy.company = request.user.company
            vacancy.published_at = datetime.now().date()
            vacancy.save()
            context = {

                "form": vacancy_form,
                "success_send": True,
            }
            return render(request, self.template_name, context)
        else:
            context = {

                "form": vacancy_form
            }
            return render(request, self.template_name, context)


class CreateVacancyView(View):
    template_name = 'vacancy-create.html'

    @method_decorator(login_required)
    def get(self, request, **argv):
        vacancy_form = MyVacancyEditForm()
        context = {
            "form": vacancy_form,
            "vacancy": {'title': "Создайте новую вакансию"},
        }
        return render(request, self.template_name, context)

    def post(self, request, **argv):
        vacancy_form = MyVacancyEditForm(request.POST)
        success_url = '/mycompany/vacancies/'
        if vacancy_form.is_valid():
            vacancy = vacancy_form.save(commit=False)
            vacancy.company = request.user.company
            vacancy.published_at = datetime.now().date()
            vacancy.save()
            return HttpResponseRedirect(success_url)

        else:
            context = {

                "form": vacancy_form
            }
            return render(request, self.template_name, context)
