from django.contrib import admin


# Register your models here.
from vacancies.models import Company, Specialty, Application, Vacancy


class CompanyAdmin(admin.ModelAdmin):
    pass


class SpecialtyAdmin(admin.ModelAdmin):
    pass


class ApplicationsAdmin(admin.ModelAdmin):
    pass


class VacanciesAdmin(admin.ModelAdmin):
    pass


admin.site.register(Vacancy, VacanciesAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Application, ApplicationsAdmin)
