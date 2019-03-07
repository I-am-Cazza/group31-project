from django.contrib import admin

from .models import Organisation
from .models import Job
from .models import TestQuestions
from .models import TestAnswers
from .models import CV
from .models import AppUser
from .models import Application
from .models import MLModel
from .models import MLcv

admin.site.register(Organisation)
admin.site.register(Job)
admin.site.register(TestQuestions)
admin.site.register(TestAnswers)
admin.site.register(CV)
admin.site.register(Application)
admin.site.register(MLcv)
admin.site.register(AppUser)


class MLModelAdmin(admin.ModelAdmin):
    add_form_template = 'employerportal/new_model.html'


admin.site.register(MLModel, MLModelAdmin)

