from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
# Create your views here.
def index(request):
    context = {"home_page": "active"}
    return render(request, 'pages/layouts/index.html', context)
def signup(request):
    context = {"signup_page": "active"}
    return render(request, 'pages/layouts/signup.html', context)
def login(request):
    context = {"login_page": "active"}
    return render(request, 'pages/layouts/login.html', context)
