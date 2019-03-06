from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.forms import UserCreationForm
from app.models import Job, AppUser, TestQuestions, Application, CV, TestAnswers, MLModel, MLcv, Organisation
from .forms import AddUserForm, LoginUserForm, SignUpForm, CvCreationForm, TestForm, SettingsForm
from app.mlengine.mlengine import train, predict
from django.http import HttpResponseForbidden
from app.views import search
import json
from .permissions import mlmodel_add_permission, job_view_permission, application_view_permission


def index(request):
    if 'id' in request.session:
        if (AppUser.objects.get(id=request.session['id']).userType)=='Employer':
            return employer_index(request)
        else:
            return applicant_jobs(request)
    else:
        job_filter = search(request)
        context = {"home_page": "active", "job_list": Job.objects.all(), 'filter': job_filter}
        return render(request, 'global/index.html', context)


def filtered_index(request):
    useremail = AppUser.objects.get(id=request.session['id']).email
    job_filter = search(request)
    context = {"home_page": "active", "job_list": job_filter, 'filter': job_filter, "email": useremail}
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
        organisation = requested_job.organisation
        completedCv = user.cvComplete
        context = {"email": useremail, "job": requested_job, 'cv': completedCv, 'organisation': organisation}
        if Application.objects.filter(user=user, job=requested_job).exists():
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
                    question_answer_list.append(form.cleaned_data['extra_questionfield_' + str(i)])
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
        correct_answer_count = 0
        for i in range(len(question_id_list)):
            correct_answer = TestQuestions.objects.get(id=question_id_list[i]).question_answer
            if question_answer_list[i].lower() == correct_answer.lower():
                correct_answer_count += 1
        correct_answer_percentage = (correct_answer_count / len(question_id_list)) * 100
        request.session['success'] = correct_answer_percentage
        if make_application(request, job_id):
            recent_application = Application.objects.all().order_by('-id')[0]
            for i in range(len(question_id_list)):
                answer = TestAnswers(application = recent_application, question = TestQuestions.objects.get(id=question_id_list[i]), answer_text = question_answer_list[i])
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
        dictCv = json.loads(cv)
        dictCv['Answer Percentage'] = request.session['success']
        job = Job.objects.get(pk=jobid)

        model = MLModel.objects.get(model_name=job.industry_type)
        model_cvs = MLcv.objects.filter(model=model)

        if len(model_cvs) > 20:  # Don't predict until MLModel dataset is > 20 cvs
            private_classification = predict(job.industry_type.model_name, dictCv)
            print("This is the classification", private_classification)
        else:
            private_classification = "not_set"
        application = Application(user=user, job=job, status='Applied', classification=private_classification, answer_percent=request.session['success'])
        application.save()
        request.session['success'] = None
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
                    hobbylist.append(dict(Name = form.cleaned_data['extra_charfield_hobby_' + str(i+1)], Interest = form.cleaned_data['extra_intfield_hobby_' + str(i+1)]))
                for i in range(int(qualificationsnumber)):
                    quallist.append(dict(Qualification = form.cleaned_data['extra_charfield_qual_' + str(i+1)], Grade = form.cleaned_data['extra_intfield_qual_' + str(i+1)]))
                for i in range(int(jobsnumber)):
                    Length = "Length of Employment"
                    joblist.append({"Company" : form.cleaned_data['extra_charfield_job_' + str(i+1)], "Position" : form.cleaned_data['extra_intfield_job_' + str(i+1)], "Length of Employment" : form.cleaned_data['extra_lenfield_job_'+ str(i+1)]})
                Languages = "Languages Known"
                Employment = "Previous Employment"
                finalobject = {"Name" : formname, "Degree Qualification" : formdegree, "Degree Level" : formlevel, "University Attended" : formuniversity, "Skills" :skillslist, "Languages Known" : langlist, "Hobbies":hobbylist, "A-Level Qualifications": quallist, "Previous Employment" : joblist}
                jsonobject = json.dumps(finalobject)
                if completedCv:
                    oldCV = CV.objects.get(owner=AppUser.objects.get(id=request.session['id']))
                    oldCV.delete()
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
            first_name= form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
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
            user = AppUser.objects.get(email=email)
            if user.userType == 'Employer':
                if user is not None:
                    if user.password==password:
                        request.session['id'] = user.id
                        return employer_index(request)
            if check_password(password, password_hash)==False:
                context= {'form': form, 'login_page': 'active','error_message':'<p style="color:red">Password is incorrect.</p>'}
                return render(request,'applicantportal/login.html',context )
            user = AppUser.objects.get(email=email)
            request.session['id'] = user.id
            if user.userType == 'Employer':
                return redirect('/admin/index')
            return applicant_jobs(request)
        else:
            return login(request)
    else:
        return login(request)


def applied_jobs(request):
    if 'id' in request.session:
        id = request.session['id']
        user = AppUser.objects.get(id=id)
        applications = Application.objects.filter(user=user)
        jobs = []
        for i in applications:
            jobs.append([i.job, i.status, i.classification.lower()])
            #jobs.append
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
        if request.method == 'POST':
            form = SettingsForm(request.POST)
            if form.is_valid():
                product = AppUser.objects.get(id=user.id)
                product.email=form.cleaned_data.get('email')
                product.first_name=form.cleaned_data.get('first_name')
                product.last_name=form.cleaned_data.get('last_name')
                product.save()
                password_hash = user.password
                old_password_form=form.cleaned_data.get('old_password')
                if bool(form.data.get('old_password', False))!=False:
                    if check_password(old_password_form, password_hash)==True:
                        new_password=form.cleaned_data.get('password')
                        confirm_password=form.cleaned_data.get('confirm_password')
                        if new_password==confirm_password:
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


def employer_index(request):
    user = check_employer(request)
    if user is not None:
        if job_view_permission(request):
            job_list = Job.objects.all()
            context = {'job_list': job_list, 'userid': user.pk, 'home_page': 'active'}
            return render(request, 'employerportal/index.html', context)
    return HttpResponseForbidden()


def employer_job(request, job_id):
    user = check_employer(request)
    if user is not None:
        if application_view_permission(request):
            job = Job.objects.get(id=job_id)
            application_list = Application.objects.filter(job=job)
            context = {'user': user, 'job': job, 'application_list': application_list}
            return render(request, 'employerportal/job.html', context)
    return HttpResponseForbidden()


def employer_job_applicant(request, job_id, applicant_id):
    user = check_employer(request)
    if user is not None:
        applicant = AppUser.objects.get(id=applicant_id)
        cv = CV.objects.get(owner=applicant)
        context = {'applicant': applicant, 'cv': cv,"job_id":job_id}
        return render(request, 'employerportal/applicant.html', context)
    else:
        return HttpResponseForbidden()


def applicant_feedback(request, job_id, applicant_id):
    user = check_employer(request)
    if user is not None:
        if request.method == 'POST':
            classification = request.POST['classification']
            ml_model = Job.objects.get(id=job_id).industry_type
            cv_user = AppUser.objects.get(id=applicant_id)
            user_application = Application.objects.get(user=cv_user, job=job_id)
            user_application.classification = classification
            user_application.save()
            cv = CV.objects.get(owner=cv_user).cvData  # Get applicant's CV
            json_cv = json.loads(cv)
            json_cv['Answer Percentage'] = user_application.answer_percent
            json_cv['Classification'] = classification  # Append classification to CV
            new_mlcv = MLcv.objects.create(model=ml_model, cv=json_cv)  # Add modified cv to ML data
            return redirect('../.')
    else:
        return HttpResponseForbidden()


def train_model(request):
    user = check_employer(request)
    if user is not None:
        if request.method == 'POST':
            model_name = request.POST['model']
            model = MLModel.objects.get(model_name=model_name)
            cvs = MLcv.objects.filter(model=model)
            training_data = []
            for i in cvs:
                training_data.append(i.cv)
            train(model_name, training_data)
            return redirect('./index/')
    else:
        return HttpResponseForbidden()
    # Create new model of same name from MLEngine


def create_new_model(request):
    user = check_employer(request)
    if user is not None:
        if mlmodel_add_permission(request):
            if request.method == 'POST':
                model_name = request.POST['model_name']
                if MLModel.objects.filter(model_name=model_name).exists():
                    context = {'new_model_page': 'active', 'error_message': '<p style="color:red">That is already a model name. Please choose a different name</p>'}
                    return render(request, 'employerportal/new_model.html', context)
                new_model = MLModel.objects.create(model_name=model_name)
                return redirect('/admin/new_model/' + model_name + '/0')
            return redirect('/admin/new_model')
    return HttpResponseForbidden()


def new_model(request):
    user = check_employer(request)
    if user is not None:
        if mlmodel_add_permission(request):
            context = {'new_model_page': 'active'}
            return render(request, 'employerportal/new_model.html', context)
    return HttpResponseForbidden()


def new_model_data(request, model_name, cv_index):
    user = check_employer(request)
    if user is not None:
        if mlmodel_add_permission(request):
            f = open("./app/mlengine/100cvDataset" + ".json", "r")
            dataset = json.loads(f.read())
            if request.method == 'POST':
                # Add classifcation to cv in model
                model = MLModel.objects.get(model_name=model_name)
                classified_cv = dataset[cv_index-1]
                classified_cv['Classification'] = request.POST['classification']
                MLcv.objects.create(model=model, cv=classified_cv)
            context = {'cv': dataset[cv_index], 'next_index': cv_index+1}
            return render(request, 'employerportal/classify_cv.html', context)
    return HttpResponseForbidden()


def check_employer(request):
    if request.user:
        user = request.user
        if user.is_authenticated:
            return user
    if 'id' in request.session:
        user = AppUser.objects.get(id=request.session['id'])
        if user.userType == 'Employer':
            return user
    else:
        return None
