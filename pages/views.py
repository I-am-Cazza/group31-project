from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
# Create your views here.
def index(request):
    context = {"home_page": "active"}
    return render(request, 'global/index.html', context)
def signup(request):
    form = UserCreationForm()
    # context = {'form': form}
    # return render(request, 'pages/layouts/signup.html', context)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return render('global/index.html')
    context={'form': form,'signup_page': 'active'}
    return render(request, 'applicantportal/signup.html',context )
def login(request):
    context = {"login_page": "active"}
    return render(request, 'applicantportal/login.html', context)
