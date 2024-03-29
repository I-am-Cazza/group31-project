# navbar_demo/pages/urls.py
from django.urls import path, re_path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('index.html', views.index, name='index'),
    re_path(r'^filter*', views.filtered_index, name='filter_index'),
    path('signup/', views.aaron_signup, name='aaron_signup'),
    re_path(r'^login/$', views.aaron_login, name='aaron_login'),
    path('applicant/', views.applicant_jobs, name='applicant_jobs'),
    path('logout/', views.logout, name='logout'),
    path('applicant/<int:job_id>', views.job, name='job'),
    path('applicant/apply/<int:job_id>/', views.apply, name='apply'),
    path('applicant/test/<int:job_id>/', views.test, name='test'),
    path('applicant/cv/', views.cv, name='cv'),
    path('applicant/applied_jobs', views.applied_jobs, name='applied_jobs'),
    path('applicant/applicant_settings', views.applicant_settings, name='applicant_settings'),
    path('admin/index/', views.employer_index, name='employer_index'),
    path('admin/train', views.train_model, name='train_model'),
    path('admin/create_new_model', views.create_new_model, name='create_new_model'),
    path('admin/new_model/', views.new_model, name='new_model'),
    path('admin/new_model/<str:model_name>/<int:cv_index>/', views.new_model_data, name='new_model_data'),
    path('admin/index/<int:job_id>/<int:applicant_id>/feedback', views.applicant_feedback, name='applicant_feedback'),
    path('admin/index/<int:job_id>/<int:applicant_id>/', views.employer_job_applicant, name='employer_job_applicant'),
    path('admin/index/<int:job_id>/', views.employer_job, name='employer_job'),
]
