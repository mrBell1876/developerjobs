from django.urls import path

from vacancies.views import CompanyView, VacancyView, VacanciesAllView, VacanciesSpecialView, SendApplicationView, \
    MyCompanyView, MyVacanciesView, EditVacancyView

urlpatterns = [
    path('vacancies/', VacanciesAllView.as_view(), name="vacancies_all"),
    path('vacancies/cat/<str:specialisation>/', VacanciesSpecialView.as_view(), name="vacancies_special"),
    path('vacancies/<int:id_vacancy>/', VacancyView.as_view(), name="vacancy"),
    path('vacancies/<int:id_vacancy>/send/', SendApplicationView.as_view(), name="send_application"),
    path('company/<int:id_company>/', CompanyView.as_view(), name="company"),
    path('mycompany/', MyCompanyView.as_view(), name="my_company"),
    path('mycompany/vacancies/', MyVacanciesView.as_view(), name="my_vacancies"),
    path('mycompany/vacancies/<vacancy_id>/', EditVacancyView.as_view(), name="edit_vacancy"),
    ]
