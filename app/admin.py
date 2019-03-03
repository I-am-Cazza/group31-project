from django.contrib import admin

from .models import Organisation
from .models import Job
from .models import TestQuestions
from .models import CV
from .models import AppUser
from .models import Application
from .models import MLModel
from .models import MLcv

admin.site.register(Organisation)
admin.site.register(Job)
admin.site.register(TestQuestions)
admin.site.register(CV)
admin.site.register(AppUser)
admin.site.register(Application)
admin.site.register(MLModel)
admin.site.register(MLcv)
