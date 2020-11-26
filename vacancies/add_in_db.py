import os
import django

os.environ["DJANGO_SETTINGS_MODULE"] = 'developerjobs.settings'
django.setup()

from vacancies.data import companies, jobs, specialties
from vacancies.models import Company, Vacancy, Specialty

if __name__ == '__main__':
    for company in companies:
        add_company = Company.objects.create(
            name=company["title"],
            location=company["location"],
            description=company["description"],
            employee_count=company["employee_count"],
        )

    for special in specialties:
        add_special = Specialty.objects.create(
            code=special["code"],
            title=special["title"]
        )

#    for job in jobs:
#       Vacancy.objects.create(
#            title=job["title"],
#            specialty=Specialty.objects.get(code=job["specialty"]),
#            company=job["company"],
 #           skills=job["skills"],
  #          description=job["description"],
   #         salary_min=job["salary_from"],
    #        salary_max=job["salary_to"],
     #       published_at=job["posted"],
      #  )
