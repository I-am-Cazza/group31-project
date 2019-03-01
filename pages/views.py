from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.forms import UserCreationForm
from app.models import Job, AppUser, TestQuestions, Application, CV, TestAnswers
from .forms import AddUserForm, LoginUserForm, SignUpForm, CvCreationForm, TestForm ,SettingsForm
from app.mlengine.mlengine import train, predict
from django.http import HttpResponseForbidden
from app.views import search
import json


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
        user = AppUser.objects.get(id=request.session['id'])
        useremail = user.email
        requested_job = Job.objects.get(id=job_id)
        completedCv = user.cvComplete
        context = {"email": useremail, "job": requested_job, 'cv': completedCv}
        if Application.objects.filter(userid=user, jobid=requested_job).exists():
            context['has_applied'] = True
        return render(request, 'applicantportal/job.html', context)
    else:
        return HttpResponseForbidden()


def test(request, job_id):
    if 'id' in request.session:
        useremail = AppUser.objects.get(id=request.session['id']).email
        requested_job = Job.objects.get(id=job_id)
        valid_questions = TestQuestions.objects.filter(question_industry=requested_job.industry_type)
        question_text_list = []
        for question in valid_questions:
            question_text_list.append(question.question_text)
        if request.method == "POST":
            form = TestForm(request.POST, extraquestion=len(valid_questions), extranames=question_text_list)
            if form.is_valid():
                question_id_list = []
                question_answer_list=[]
                for question in valid_questions:
                    question_id_list.append(int(question.id))
                for i in range(len(valid_questions)):
                    question_answer_list.append(form.cleaned_data['extra_questionfield_' +str(i)])
                # TODO store test results in database
                return apply(request, job_id, question_id_list, question_answer_list)
            else:
                context = {"email": useremail, "job": requested_job, "questions": valid_questions, "form": form, "error": True}
                return render(request, 'applicantportal/test.html', context)
        else:
            form = TestForm(extraquestion=len(valid_questions), extranames=question_text_list)
            context = {"email" : useremail, "job": requested_job, "questions": valid_questions, "form": form}
            return render(request, 'applicantportal/test.html', context)
    else:
        return HttpResponseForbidden()


def apply(request, job_id, question_id_list, question_answer_list):
    if 'id' in request.session:
        id = request.session['id']
        if make_application(request, job_id):
            recent_application = Application.objects.all().order_by('-id')[0]
            for i in range(len(question_id_list)):
                answer = TestAnswers(applicationid = recent_application, questionid = TestQuestions.objects.get(id=question_id_list[i]), answer_text = question_answer_list[i])
                answer.save()
            return redirect('applied_jobs')
            # TODO Success message for adding application
        else:
            return redirect('../../')  # TODO Error message for application not made...
    else:
        return HttpResponseForbidden()


def make_application(request, jobid):
        userid = request.session['id']
        user = AppUser.objects.get(pk=userid)
        cv = CV.objects.get(owner=userid).cvData
        #private_classification = predict("demo", cv)[0]
        private_classification = "test"
        print("This is the classification", private_classification)
        job = Job.objects.get(pk=jobid)
        application = Application(userid=user, jobid=job, status='Applied', classification=private_classification)
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
                formdegree = form.cleaned_data['degree']
                formlevel = form.cleaned_data['degree_level']
                formuniversity = form.cleaned_data['university']
                skillslist = []
                langlist = []
                hobbylist = []
                quallist = []
                joblist = []
                for i in range(int(skillsnumber)):
                    skillslist.append(dict(Skill = form.cleaned_data['extra_charfield_' + str(i+1)], Expertise = form.cleaned_data['extra_intfield_' + str(i+1)]))
                for i in range(int(languagesnumber)):
                    langlist.append(dict(Language = form.cleaned_data['extra_charfield_lang_' + str(i+1)], Expertise = form.cleaned_data['extra_intfield_lang_' + str(i+1)]))
                for i in range(int(hobbiesnumber)):
                    hobbylist.append(dict(Hobby = form.cleaned_data['extra_charfield_hobby_' + str(i+1)], Interest = form.cleaned_data['extra_intfield_hobby_' + str(i+1)]))
                for i in range(int(qualificationsnumber)):
                    quallist.append(dict(Qualification = form.cleaned_data['extra_charfield_qual_' + str(i+1)], Grade = form.cleaned_data['extra_intfield_qual_' + str(i+1)]))
                for i in range(int(jobsnumber)):
                    joblist.append(dict(Company = form.cleaned_data['extra_charfield_job_' + str(i+1)], Position = form.cleaned_data['extra_intfield_job_' + str(i+1)], Length = form.cleaned_data['extra_lenfield_job_'+ str(i+1)]))
                finalobject = dict(Name = formname, Degree = formdegree, Level = formlevel, University = formuniversity, Skills=skillslist, Languages = langlist, hobbies=hobbylist, Qualifications = quallist, Employment = joblist)
                jsonobject = json.dumps(finalobject)
                newCV = CV(owner=AppUser.objects.get(id=request.session['id']), cvData=jsonobject)
                newCV.save()
                AppUser.objects.filter(id=request.session['id']).update(cvComplete=True)
                #context = {"job_list": Job.objects.all(), "email": useremail, "cv": True}
                return applicant_jobs(request)
            else:
                context = {"CV":"active","email" : useremail, "form": form, "cv": completedCv, "error": "Please fill out the form correctly"}
                return render(request, 'applicantportal/cv.html', context)
        else:
            form = CvCreationForm()
            context = {"CV":"active","email" : useremail, "form": form, "cv": completedCv}
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
            # first_name= form.cleaned_data['first_name']
            # last_name=form.cleaned_data['last_name']
            if AppUser.objects.filter(email=email).exists():
                context= {'form': form, 'signup_page': 'active','error_message':'<p style="color:red">This email already exsists.</p>'}
                return render(request,'applicantportal/signup.html',context )
            if len(password)<8:
                context= {'form': form, 'signup_page': 'active','error_message':'<p style="color:red">Password length is too short. Password must be greater than 8 characters.</p>'}
                return render(request,'applicantportal/signup.html',context )
            if password!=check_password:
                context= {'form': form, 'signup_page': 'active','error_message':'<p style="color:red">Passwords do not match.</p>'}
                return render(request,'applicantportal/signup.html',context )
            if any(x.isupper() for x in password)==False:
                context= {'form': form, 'signup_page': 'active','error_message':'<p style="color:red">Password needs one uppercase letter.</p>'}
                return render(request,'applicantportal/signup.html',context )
            hashed_password = make_password(password)
            user = AppUser(email=email, password=hashed_password, userType='Applicant',first_name=first_name,last_name=last_name)
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
            jobs.append([i.jobid, i.status])
            jobs.append
        useremail = user.email
        completedCv = user.cvComplete
        context = {"applied_jobs":"active",'job_list': jobs, 'user': user, 'email': useremail, 'cv': completedCv}
        return render(request, 'applicantportal/applied_jobs.html', context)
    else:
        return HttpResponseForbidden()

def applicant_settings(request):
    if 'id' in request.session:
        user=AppUser.objects.get(id=request.session['id'])
        email=user.email
        first_name=user.first_name
        last_name=user.last_name
        # country=user.country
        # city=user.city
        # address_line_1=user.address_line_1
        # address_line_2=user.address_line_2
        # postal_code=user.postal_code
        # phone_number=user.phone_number
        if request.method == 'POST':
            form = SettingsForm(request.POST)
            if form.is_valid():
                print(user.id)
                product = AppUser.objects.get(id=user.id)
                product.email=form.cleaned_data.get('email')
                product.first_name=form.cleaned_data.get('first_name')
                product.last_name=form.cleaned_data.get('last_name')
                # product.country=form.cleaned_data.get('country')
                # product.city=form.cleaned_data.get('city')
                # product.address_line_1=form.cleaned_data.get('address_line_1')
                # product.address_line_2=form.cleaned_data.get('address_line_2')
                # product.postal_code=form.cleaned_data.get('postal_code')
                # product.phone_number=form.cleaned_data.get('phone_number')
                product.save()
                password_hash = user.password
                old_password_form=form.cleaned_data.get('old_password')
                if bool(form.data.get('old_password', False))!=False:
                    if check_password(old_password_form, password_hash)==True:
                        new_password=form.cleaned_data.get('password')
                        confirm_password=form.cleaned_data.get('confirm_password')
                        print(new_password)
                        print(confirm_password)
                        if new_password==confirm_password:
                            print(new_password)
                            print(confirm_password)
                            if len(new_password)<8:
                                context= {'form': form, 'applicant_settings': 'active','error_message':'<p style="color:red">Password length is too short. Password must be greater than 8 characters.</p>'}
                                return render(request,'applicantportal/applicant_settings.html',context )
                            if any(x.isupper() for x in new_password)==False:
                                context= {'form': form, 'applicant_settings': 'active','error_message':'<p style="color:red">Password needs one uppercase letter.</p>'}
                                return render(request,'applicantportal/applicant_settings.html',context )
                            product.password=make_password(new_password)
                            product.save()
                            return applicant_jobs(request)
                        else:
                            context= {'form': form, 'applicant_settings': 'active','error_message':'<p style="color:red">Passwords do not match</p>'}
                            return render(request,'applicantportal/applicant_settings.html',context )
                    else:
                        context= {'form': form, 'applicant_settings': 'active','error_message':'<p style="color:red">Old password does not match with exisisting password</p>'}
                        return render(request,'applicantportal/applicant_settings.html',context )
                else:
                    return applicant_jobs(request)
        else:
            form=SettingsForm(initial={'email':email,'first_name':first_name,'last_name':last_name})
            context = {'form': form, 'signup_page': 'active', 'email': email}
            return render(request, 'applicantportal/applicant_settings.html', context)

        return render(request, 'applicantportal/applicant_settings.html')


def employer_index(request, user_id):
        userType = AppUser.objects.get(id=user_id).userType
        if userType == 'Employer':
            job_list = Job.objects.all()
            context = {'job_list': job_list, 'userid': user_id}
            return render(request, 'employerportal/index.html', context)
        else:
            return HttpResponseForbidden()


def employer_job(request, user_id, job_id):
    userType = AppUser.objects.get(id=user_id).userType
    if userType == 'Employer':
        job = Job.objects.get(id=job_id)
        application_list = Application.objects.filter(jobid=job)
        context = {'job': job, 'application_list': application_list}
        return render(request, 'employerportal/job.html', context)
    else:
        return HttpResponseForbidden()


def employer_job_applicant(request, user_id, job_id, applicant_id):
    userType = AppUser.objects.get(id=user_id).userType
    if userType == 'Employer':
        applicant = AppUser.objects.get(id=applicant_id)
        cv = CV.objects.get(owner=applicant)
        context = {'applicant': applicant, 'cv': cv}
        return render(request, 'employerportal/applicant.html', context)
    else:
        return HttpResponseForbidden()
