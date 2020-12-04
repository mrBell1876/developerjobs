from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, Layout, Row, Column
from django import forms
from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator
from django.forms import ModelForm

from vacancies.models import Company, Vacancy, Resume

PATTERN_PHONE_VALIDATOR = RegexValidator(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$',
                                         "Введите номер вида +7 XXX XXX XX XX")


class RegisterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Зарегистрироваться', css_class='btn btn-primary btn-lg btn-block'))

        self.helper.form_class = 'form-label-group form-signin pt-5'
        self.helper.label_class = 'text-muted'

    first_name = forms.CharField(min_length=2, max_length=20, label="Имя")
    last_name = forms.CharField(min_length=2, max_length=20, label="Фамилия")
    login = forms.CharField(min_length=3, label="Логин", required='autofocus')
    password = forms.CharField(min_length=6, label="Пароль", widget=forms.PasswordInput())


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Войти', css_class='btn btn-primary btn-lg btn-block'))
        self.helper.form_class = 'form-label-group form-signin pt-5'
        self.helper.label_class = 'text-muted'


class ApplicationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Отправить отклик', css_class='btn btn-primary mt-4 mb-2'))

        self.helper.form_class = 'form-label-group  pt-5'
        self.helper.label_class = 'mb-1'

    name = forms.CharField(min_length=2, max_length=20, label="Вас зовут")
    phone = forms.CharField(min_length=6, max_length=12, label="Телефон", validators=[PATTERN_PHONE_VALIDATOR])
    message = forms.CharField(widget=forms.Textarea, label="Сопроводительное сообщение")


class MyCompanyEditForm(ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'logo', 'employee_count', 'location', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper = FormHelper()

        self.helper.form_method = 'post'
        self.helper.layout = Layout(

            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('logo', css_class='form-group col-md-6 mb-0'),
                css_class='form-row',
            ),
            Row(
                Column('employee_count', css_class='form-group col-md-6 mb-0'),
                Column('location', css_class='form-group col-md-6 mb-0'),
                css_class='form-row',
            ),
            Row(
                Column('description', css_class='form-group mb-0'),
                css_class='form-row',
            ),
            FormActions(
                Submit('submit', 'Сохранить'),
            )
        )


class ApplicationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Отправить отклик', css_class='btn btn-primary mt-4 mb-2'))

        self.helper.form_class = 'form-label-group  pt-5'
        self.helper.label_class = 'mb-1'

    name = forms.CharField(min_length=2, max_length=20, label="Вас зовут")
    phone = forms.CharField(min_length=6, max_length=12, label="Телефон", validators=[PATTERN_PHONE_VALIDATOR])
    message = forms.CharField(widget=forms.Textarea, label="Сопроводительное сообщение")


class MyVacancyEditForm(ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title', 'specialty', 'skills', 'description', 'salary_min', 'salary_max']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper = FormHelper()

        self.helper.form_method = 'post'
        self.helper.layout = Layout(

            Row(
                Column('title', css_class='form-group col-md-6 mb-0'),
                Column('specialty', css_class='form-group col-md-6 mb-0'),
                css_class='form-row',
            ),
            Row(
                Column('salary_min', css_class='form-group col-md-6 mb-0'),
                Column('salary_max', css_class='form-group col-md-6 mb-0'),
                css_class='form-row',
            ),
            Row(
                Column('skills', css_class='form-group mb-0'),
                css_class='form-row',
            ),
            Row(
                Column('description', css_class='form-group mb-0'),
                css_class='form-row',
            ),
            FormActions(
                Submit('submit', 'Сохранить'),
            )
        )

class MyResumeEditForm(ModelForm):
    class Meta:
        model = Resume
        fields = ['name', 'surname', 'status_CHOISES', 'salary', 'grade',
                  'education', 'specialty', 'experience', 'portfolio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper = FormHelper()

        self.helper.form_method = 'post'
        self.helper.layout = Layout(

            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('surname', css_class='form-group col-md-6 mb-0'),
                css_class='form-row',
            ),
            Row(
                Column('status_CHOISES', css_class='form-group col-md-6 mb-0'),
                Column('salary', css_class='form-group col-md-6 mb-0'),
                css_class='form-row',
            ),


            Row(
                Column('specialty', css_class='form-group mb-0'),
                Column('grade', css_class='form-group mb-0'),
                css_class='form-row',

            ),
            Row(
                Column('education', css_class='form-group mb-0'),
                css_class='form-row',
            ),
            Row(
                Column('experience', css_class='form-group mb-0'),
                css_class='form-row',
            ),
            Row(
                Column('portfolio', css_class='form-group mb-0'),
                css_class='form-row',
            ),
            FormActions(
                Submit('submit', 'Сохранить'),
            )
        )

class SearchForm(forms.Form):
    find = forms.CharField(min_length=2, max_length=40, label=False,
                           widget=forms.TextInput(attrs={'placeholder': "найти работу или стажировку"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper = FormHelper()
        self.helper.form_action = "/search/"
        self.helper.form_method = 'get'
        # self.helper.add_input(Submit('submit', 'Найти', css_class='btn btn-primary mt-4 mb-2'))

        self.helper.layout = Layout(
            Row(
                Column('find', css_class='form-group col-8 col-md-10 pl-0'),

                Column(
                    FormActions(
                        Submit('submit', 'Найти', css_class='btn btn-primary w-100'),
                    ),
                    css_class='form-group col-4 col-md-2 pl-0')
            ),
        )
