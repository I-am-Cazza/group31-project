from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.forms import UserCreationForm
from app.models import Job, AppUser
from .forms import SignUpForm, AddUserForm, LoginUserForm


def index(request):
    context = {"home_page": "active", "job_list": Job.objects.all()}
    return render(request, 'global/index.html', context)

def applicant_jobs(request):
    context = {"job_list": Job.objects.all()}
    return render(request, 'applicantportal/jobs.html', context)

def aaron_signup(request):
    form = AddUserForm()
    context = {'form': form, 'signup_page': 'active'}
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']  # TODO check email is unique, only store unique emails
            password = form.cleaned_data['password']
            check_password = form.cleaned_data['confirm_password']
            if password == check_password:
                hashed_password = make_password(password)
                user = AppUser(email=email, password=hashed_password, userType='Applicant')
                user.save()  # TODO create session key
                return redirect('index')
    return render(request, 'applicantportal/signup.html', context)


# def signup(request):
#     form = SignUpForm()
#     # context = {'form': form}
#     # return render(request, 'pages/layouts/signup.html', context)
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             auth_login(request, user)
#             return redirect('index')
#     context = {'form': form, 'signup_page': 'active'}
#     return render(request, 'applicantportal/signup.html', context)


def login(request):
    form = LoginUserForm()
    context = {'form': form, 'login_page': 'active'}
    return render(request, 'pages/templates/applicantportal/login.html', context)


def aaron_login(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if AppUser.objects.filter(email=email).exists():
                password_hash = AppUser.objects.get(email=email).password
                if check_password(password, password_hash):
                    return render(request, 'applicantportal/home.html')  # TODO create session key
                else:
                    return login(request)
            else:
                return login(request)  # TODO email not registered error
        else:
            return login(request)
    else:
        return login(request)
