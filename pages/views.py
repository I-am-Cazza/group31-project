from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
# Create your views here.
def index(request):
    context = {"home_page": "active"}
    return render(request, 'pages/layouts/index.html', context)
def signup(request):
    # context = {'form': form}
    # return render(request, 'pages/layouts/signup.html', context)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('pages/layouts/index.html')
    else:
        form = UserCreationForm()
    return render(request, 'pages/layouts/signup.html', {'form': form})
def login(request):
    context = {"login_page": "active"}
    return render(request, 'pages/layouts/login.html', context)
