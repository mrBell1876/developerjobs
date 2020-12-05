from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from vacancies.forms import MyResumeEditForm
from vacancies.models import Resume


class MyResume(View):
    template_name = 'resume-edit.html'
    start_url = 'letsstart/'

    @method_decorator(login_required)
    def get(self, request, **argv):
        if not Resume.objects.filter(user=request.user):
            return HttpResponseRedirect(self.start_url)

        resume = Resume.objects.get(user=request.user)
        resume_form = MyResumeEditForm(instance=resume)
        context = {
            "form": resume_form
        }
        return render(request, self.template_name, context)

    def post(self, request, **argv):
        resume = Resume.objects.get(user=request.user)
        resume_form = MyResumeEditForm(request.POST, instance=resume)

        if resume_form.is_valid():
            resume = resume_form.save(commit=False)
            resume.user = request.user
            resume.save()
            messages.success(request, 'Информация о вакансии обновлена')
            context = {

                "form": resume_form,
            }
            return render(request, self.template_name, context)
        else:
            context = {

                "form": resume_form
            }
            return render(request, self.template_name, context)


class MyResumeStart(View):
    template_name = 'resume-lets-start.html'

    @method_decorator(login_required)
    def get(self, request, **argv):
        return render(request, self.template_name)


class MyResumeCreate(View):
    template_name = 'resume-create.html'
    resume_form = MyResumeEditForm
    success_url = '/myresume/'

    @method_decorator(login_required)
    def get(self, request, **argv):
        if Resume.objects.filter(user=request.user):
            return HttpResponseRedirect(self.success_url)
        context = {
            "form": self.resume_form
        }
        return render(request, self.template_name, context)

    def post(self, request, **argv):
        resume_form = MyResumeEditForm(request.POST)
        if resume_form.is_valid():
            messages.success(request, 'Резюме успешно создано')
            resume = resume_form.save(commit=False)
            resume.user = request.user
            resume.save()
            return HttpResponseRedirect(self.success_url)
        else:
            context = {

                "form": resume_form
            }
            return render(request, self.template_name, context)


