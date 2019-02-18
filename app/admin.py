from django.contrib import admin

from .models import Organisation
from .models import Job
from .models import TestQuestions

admin.site.register(Organisation)
admin.site.register(Job)
admin.site.register(TestQuestions)


# Register your models here.
