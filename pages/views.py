from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm
from app.models import Job, AppUser
from .forms import SignUpForm, AddUserForm, LoginUserForm


def index(request):
    context = {"home_page": "active", "job_list": Job.objects.all()}
    return render(request, 'global/index.html', context)


def aaron_signup(request):
    form = AddUserForm()
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            check_password = form.cleaned_data['confirm_password']
            if password == check_password:
                hashed_password = make_password(password)
                user = AppUser(email=email, password=hashed_password, userType='Applicant')
                user.save()
                return redirect('index')
        context = {'form': form, 'signup_page': 'active'}
        return render(request, 'applicantportal/signup.html', context)


def signup(request):
    form = SignUpForm()
    # context = {'form': form}
    # return render(request, 'pages/layouts/signup.html', context)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('index')
    context = {'form': form, 'signup_page': 'active'}
    return render(request, 'applicantportal/signup.html', context)


def login(request):
    context = {"login_page": "active"}
    return render(request, 'applicantportal/login.html', context)
