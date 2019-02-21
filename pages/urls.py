# navbar_demo/pages/urls.py
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('index.html', views.index, name='index'),
    path('signup/', views.aaron_signup, name='aaron_signup'),
    path('login/', views.aaron_login, name='aaron_login'),
    path('applicant/', views.applicant_jobs, name='applicantjobs'),
    path('logout/', views.logout, name='logout'),
    path('applicant/<int:job_id>', views.job, name='job'),
    path('applicant/test/<int:job_id>', views.test, name='test'),
    path('applicant/cv/', views.cv, name='cv'),
    path('applicant/cv/plus', views.addskill, name='addskill'),
    path('applicant/cv/minus', views.removeskill, name='removeskill')
]
