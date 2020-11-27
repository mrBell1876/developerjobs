from django.urls import path

from vacancies.views import CompanyView, VacancyView, VacanciesAllView, VacanciesSpecialView

urlpatterns = [
    path('vacancies/', VacanciesAllView.as_view(), name="vacancies_all"),
    path('vacancies/cat/<str:specialisation>/', VacanciesSpecialView.as_view(), name="vacancies_special"),
    path('vacancies/<int:id_vacancy>/', VacancyView.as_view(), name="vacancy"),
    path('company/<int:id_company>/', CompanyView.as_view(), name="company"),
    ]
