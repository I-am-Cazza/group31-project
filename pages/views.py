from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserCreationForm
from app.models import Job
from django.contrib.auth.models import User
from .forms import SignUpForm

# Create your views here.
# Create your views here.
def index(request):
    context = {"home_page": "active", "job_list": Job.objects.all()}
    return render(request, 'global/index.html', context)

def applicant_jobs(request):
    context = {"job_list": Job.objects.all()}
    return render(request, 'applicantportal/jobs.html', context)

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
            request.session['id'] = User.objects.filter()
            return redirect('applicantjobs')
    context={'form': form,'signup_page': 'active'}
    return render(request, 'applicantportal/signup.html',context )
def login(request):
    context = {"login_page": "active"}
    return render(request, 'applicantportal/login.html', context)
