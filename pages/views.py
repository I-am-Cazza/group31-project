from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.forms import UserCreationForm
from app.models import Job, AppUser, TestQuestions, Application, CV
from app.models import Job, AppUser, TestQuestions, CV
from .forms import AddUserForm, LoginUserForm, SignUpForm, CvCreationForm
from django.http import HttpResponseForbidden
from app.views import search
import json
from itertools import chain


def index(request):
    if 'id' in request.session:
        return applicant_jobs(request)
    else:
        job_filter = search(request)
        context = {"home_page": "active", "job_list": Job.objects.all(), 'filter': job_filter}
        return render(request, 'global/index.html', context)


def filtered_index(request):
    job_filter = search(request)
    context = {"home_page": "active", "job_list": job_filter, 'filter': job_filter}
    return render(request, 'global/filter_index.html', context)


def applicant_jobs(request):
    if 'id' in request.session:
        useremail = AppUser.objects.get(id=request.session['id']).email
        completedCv = AppUser.objects.get(id=request.session['id']).cvComplete
        job_filter = search(request)
        context = {"job_list": Job.objects.all(), "email": useremail, "cv": completedCv, 'filter': job_filter}
        return render(request, 'applicantportal/jobs.html', context)
    else:
        return HttpResponseForbidden()


def job(request, job_id):
    if 'id' in request.session:
        useremail = AppUser.objects.get(id=request.session['id']).email
        requested_job = Job.objects.get(id=job_id)
        context = {"email": useremail, "job": requested_job}
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


def apply(request, job_id):
    if 'id' in request.session:
        id = request.session['id']
        cv = CV.objects.get(owner=id).cvData
        # TODO Send CV to Machine Learning
        if make_application(request, job_id):
            return redirect('../../')  # TODO Return to applicant_jobs
            # TODO Success message for adding application
        else:
            return redirect('../../')  # TODO Error message for application not made...
    else:
        return HttpResponseForbidden()


def make_application(request, jobid):
        userid = request.session['id']
        user = AppUser.objects.get(pk=userid)
        job = Job.objects.get(pk=jobid)
        application = Application(userid=user, jobid=job, status='Applied')
        application.save()
        return True


def cv(request):
    if 'id' in request.session:
        if 'skills' not in request.session:
            request.session['skills'] = 0
        useremail = AppUser.objects.get(id=request.session['id']).email
        completedCv = AppUser.objects.get(id=request.session['id']).cvComplete
        if request.method == 'POST':
            skillsnumber = request.POST.get('extra_field_count')
            languagesnumber = request.POST.get('extra_language_count')
            hobbiesnumber = request.POST.get('extra_hobby_count')
            qualificationsnumber = request.POST.get('extra_qual_count')
            jobsnumber = request.POST.get('extra_job_count')
            form = CvCreationForm(request.POST, extraskills=skillsnumber, extralang=languagesnumber, extrahobby=hobbiesnumber, extraqual=qualificationsnumber, extrajob=jobsnumber)
            if form.is_valid():
                # TODO store data in database
                formname = form.cleaned_data['name']
                skillslist = []
                langlist = []
                hobbylist = []
                quallist = []
                joblist = []
                for i in range(int(skillsnumber)):
                    skillslist.append(dict(skill = form.cleaned_data['extra_charfield_' + str(i+1)], expertise = form.cleaned_data['extra_intfield_' + str(i+1)]))
                for i in range(int(languagesnumber)):
                    langlist.append(dict(language = form.cleaned_data['extra_charfield_lang_' + str(i+1)], expertise = form.cleaned_data['extra_intfield_lang_' + str(i+1)]))
                for i in range(int(hobbiesnumber)):
                    hobbylist.append(dict(hobby = form.cleaned_data['extra_charfield_hobby_' + str(i+1)], interest = form.cleaned_data['extra_intfield_hobby_' + str(i+1)]))
                for i in range(int(qualificationsnumber)):
                    quallist.append(dict(qualification = form.cleaned_data['extra_charfield_qual_' + str(i+1)], grade = form.cleaned_data['extra_intfield_qual_' + str(i+1)]))
                for i in range(int(jobsnumber)):
                    quallist.append(dict(company = form.cleaned_data['extra_charfield_job_' + str(i+1)], grade = form.cleaned_data['extra_intfield_job_' + str(i+1)], length = form.cleaned_data['extra_lenfield_job_'+ str(i+1)]))
                finalobject = dict(name = formname, skills=skillslist, languages = langlist, hobbies=hobbylist, qualifications = quallist, jobs = joblist)
                jsonobject = json.dumps(finalobject)
                newCV = CV(owner=AppUser.objects.get(id=request.session['id']), cvData=jsonobject)
                newCV.save()
                AppUser.objects.filter(id=request.session['id']).update(cvComplete=True)
                #context = {"job_list": Job.objects.all(), "email": useremail, "cv": True}
                return applicant_jobs(request)
            else:
                context = {"email" : useremail, "form": form, "cv": completedCv, "error": "Please fill out the form correctly"}
                return render(request, 'applicantportal/cv.html', context)
        else:
            form = CvCreationForm()
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
    return redirect('index')


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
            return applicant_jobs(request)
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
            return applicant_jobs(request)
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
            if AppUser.objects.filter(email=email).exists()==False:
                context= {'form': form, 'login_page': 'active','error_message':'<p style="color:red">Email is not registered.</p>'}
                return render(request,'applicantportal/login.html',context )
            password_hash = AppUser.objects.get(email=email).password
            if check_password(password, password_hash)==False:
                context= {'form': form, 'login_page': 'active','error_message':'<p style="color:red">Password is incorrect.</p>'}
                return render(request,'applicantportal/login.html',context )
            request.session['id'] = AppUser.objects.get(email=email).id
            return applicant_jobs(request)
        else:
            return login(request)
    else:
        return login(request)


def applied_jobs(request):
    if 'id' in request.session:
        id = request.session['id']
        user = AppUser.objects.get(id=id)
        applications = Application.objects.filter(userid=user)
        jobs = []
        for i in applications:
            jobs.append(i.jobid)
        # TODO get all jobs that user has applied for
        context = {'job_list': jobs}
        return render(request, 'applicantportal/applied_jobs.html', context)
    else:
        redirect('../../')

