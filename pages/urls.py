# navbar_demo/pages/urls.py
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('applicant/', views.applicant_jobs, name='applicantjobs')
]
