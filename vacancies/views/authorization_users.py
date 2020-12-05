from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from vacancies.forms import RegisterForm, LoginForm


class MySignupView(View):
    register_form = RegisterForm
    success_url = '../login/'
    template_name = 'register.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.register_form})

    def post(self, request, *args, **kwargs):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            data = register_form.cleaned_data
            User.objects.create_user(
                username=data['login'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password=data['password']
            )
            return HttpResponseRedirect(self.success_url)
        else:
            context = {

                "form": register_form
            }
            return render(request, self.template_name, context)


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'
    form_class = LoginForm