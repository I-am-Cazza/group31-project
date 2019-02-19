# navbar_demo/pages/urls.py
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.aaron_signup, name='signup'),
    path('login/', views.login, name='login'),
]
