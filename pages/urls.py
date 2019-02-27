# navbar_demo/pages/urls.py
from django.urls import path, re_path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('index.html', views.index, name='index'),
    re_path(r'^filter*', views.filtered_index, name='filter_index'),
    path('signup/', views.aaron_signup, name='aaron_signup'),
    path('login/', views.aaron_login, name='aaron_login'),
    path('applicant/', views.applicant_jobs, name='applicant_jobs'),
    path('logout/', views.logout, name='logout'),
    path('applicant/<int:job_id>', views.job, name='job'),
    path('applicant/apply/<int:job_id>/', views.apply, name='apply'),
    path('applicant/test/<int:job_id>/', views.test, name='test'),
    path('applicant/cv/', views.cv, name='cv'),
    path('applicant/applied_jobs', views.applied_jobs, name='applied_jobs'),
    path('applicant/applicant_settings', views.applicant_settings, name='applicant_settings')
]
