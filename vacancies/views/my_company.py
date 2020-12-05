from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from vacancies.forms import MyCompanyEditForm, MyVacancyEditForm
from vacancies.models import Company, Vacancy, Application


class MyCompanyView(View):
    template_name = 'my-company.html'
    start_url = "letsstart/"

    @method_decorator(login_required)
    def get(self, request, **argv):

        if not Company.objects.filter(owner=request.user):
            return HttpResponseRedirect(self.start_url)
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
            messages.success(request, 'Информация о компании обновлена')
            context = {

                "form": company_form,
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
            messages.success(request, 'Компания успешно создана')
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
            messages.success(request, 'Вакансия успешно создана')
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
