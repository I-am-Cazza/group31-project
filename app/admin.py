from django.contrib import admin

from .models import Organisation
from .models import Job
from .models import TestQuestions
# from .models import AppUser

admin.site.register(Organisation)
admin.site.register(Job)
admin.site.register(TestQuestions)
# admin.site.register(AppUser)