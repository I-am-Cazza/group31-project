from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.forms import UserCreationForm
from app.models import Job, AppUser, TestQuestions
from .forms import AddUserForm, LoginUserForm, SignUpForm, CvCreationForm
from django.http import HttpResponseForbidden


def index(request):
    if 'id' in request.session:
        return redirect('applicantjobs')
    else:
        context = {"home_page": "active", "job_list": Job.objects.all()}
        return render(request, 'global/index.html', context)


def applicant_jobs(request):
    if 'id' in request.session:
        useremail = AppUser.objects.get(id=request.session['id']).email
        completedCv = AppUser.objects.get(id=request.session['id']).cvComplete
        context = {"job_list": Job.objects.all(), "email": useremail, "cv": completedCv}
        return render(request, 'applicantportal/jobs.html', context)
    else:
        return HttpResponseForbidden()


def job(request, job_id):
    if 'id' in request.session:
        useremail = AppUser.objects.get(id=request.session['id']).email
        requested_job = Job.objects.get(id=job_id)
        context = {"email" : useremail, "job": requested_job}
        return render(request, 'applicantportal/job.html', context)
    else:
        return HttpResponseForbidden()


def test(request, job_id):
    if 'id' in request.session:
        useremail = AppUser.objects.get(id=request.session['id']).email
        requested_job = Job.objects.get(id=job_id)
        valid_questions = TestQuestions.objects.filter(question_industry=requested_job.industry_type)
        context = {"email" : useremail, "job": requested_job, "questions": valid_questions}
        return render(request, 'applicantportal/test.html', context)
    else:
        return HttpResponseForbidden()

def cv(request):
    if 'id' in request.session:
        if 'skills' not in request.session:
            request.session['skills'] = 1
        useremail = AppUser.objects.get(id=request.session['id']).email
        completedCv = AppUser.objects.get(id=request.session['id']).cvComplete
        if request.method == 'POST':
            form = CvCreationForm(request.POST, extra=request.POST.get('extra_field_count'))
            if form.is_valid():
                #TODO store data in database
                AppUser.objects.filter(id=request.session['id']).update(cvComplete=True)
                #context = {"job_list": Job.objects.all(), "email": useremail, "cv": True}
                return redirect('applicantjobs')
            else:
                context = {"email" : useremail, "form": form, "cv": completedCv, "error": "Please fill out the form correctly"}
                return render(request, 'applicantportal/cv.html', context)
        else:
            form = CvCreationForm(extra=1)
            context = {"email" : useremail, "form": form, "cv": completedCv}
            return render(request, 'applicantportal/cv.html', context)
    else:
        return HttpResponseForbidden()

def addskill(request):
    if 'id' in request.session:
        request.session['skills'] += 1
        return redirect('cv')
    else:
        return HttpResponseForbidden()

def removeskill(request):
    if 'id' in request.session:
        request.session['skills'] -= 1
        return redirect('cv')
    else:
        return HttpResponseForbidden()

def logout(request):
    request.session.flush()
    context = {"home_page": "active", "job_list": Job.objects.all()}
    return render(request, 'global/index.html', context)


def aaron_signup(request):
    form = AddUserForm()
    context = {'form': form, 'signup_page': 'active'}
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']  # TODO check email is unique, only store unique emails
            password = form.cleaned_data['password']
            check_password = form.cleaned_data['confirm_password']
            if AppUser.objects.filter(email=email).exists():
                context= {'form': form, 'signup_page': 'active','error_message':'<p style="color:red">This email already exsists.</p>'}
                return render(request,'applicantportal/signup.html',context )
            if len(password)<8:
                context= {'form': form, 'signup_page': 'active','error_message':'<p style="color:red">Password length is too short. Password must be greater than 8 characters.</p>'}
                return render(request,'applicantportal/signup.html',context )
            if password!=check_password:
                context= {'form': form, 'signup_page': 'active','error_message':'<p style="color:red">Passwords do not match.</p>'}
                return render(request,'applicantportal/signup.html',context )
            hashed_password = make_password(password)
            user = AppUser(email=email, password=hashed_password, userType='Applicant')
            user.save()  # TODO create session key
            request.session['id'] = AppUser.objects.get(email=email).id
            return redirect('applicantjobs')
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
            request.session['id'] = AppUser.objects.get(username=username).id
            return redirect('applicantjobs')
    context = {'form': form, 'signup_page': 'active'}
    return render(request, 'applicantportal/signup.html', context)


def login(request):
    form = LoginUserForm()
    context = {'form': form, 'login_page': 'active'}
    return render(request, 'applicantportal/login.html', context)


def aaron_login(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if AppUser.objects.filter(email=email).exists():
                password_hash = AppUser.objects.get(email=email).password
                if check_password(password, password_hash):
                    request.session['id'] = AppUser.objects.get(email=email).id
                    return redirect('applicantjobs')
                else:
                    return login(request)
            else:
                return login(request)  # TODO email not registered error
        else:
            return login(request)
    else:
        return login(request)
