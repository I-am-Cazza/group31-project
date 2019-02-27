from django import forms
from django.forms import ModelForm
from app.models import AppUser, TestQuestions
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=20, required=True, help_text="*")
    first_name = forms.CharField(max_length=20, required=True, help_text='*')
    last_name = forms.CharField(max_length=30, required=True, help_text='*')
    email = forms.EmailField(max_length=254, required=True,help_text='*')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class AddUserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), max_length=50)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(), max_length=50)
    # first_name= forms.CharField(max_length=50)
    # last_name=forms.CharField(max_length=50)

    class Meta:
        model = AppUser
        fields = ['email','first_name','last_name']


class LoginUserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), max_length=50)

    class Meta:
        model = AppUser
        fields = ['email', 'password']

class SettingsForm(ModelForm):
    old_password=forms.CharField(label='Old Password',widget=forms.PasswordInput(), max_length=50,required=False)
    password = forms.CharField(label='New Password',widget=forms.PasswordInput(), max_length=50,required=False)
    confirm_password = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(), max_length=50,required=False)
    class Meta:
        model= AppUser
        fields=['email','first_name','last_name','city','country','address_line_1','address_line_2','postal_code','phone_number']

class CvCreationForm(forms.Form):
    name = forms.CharField(label='Name', max_length=50, required=True)
    university = forms.CharField(label='University Attended', max_length=100, required=False)
    degree = forms.CharField(label='Degree Qualification', max_length=100, required=False)
    degree_level = forms.CharField(label = 'Degree Level', max_length=10, required=False)
    extra_field_count = forms.CharField(widget=forms.HiddenInput())
    extra_language_count = forms.CharField(widget=forms.HiddenInput())
    extra_hobby_count = forms.CharField(widget=forms.HiddenInput())
    extra_qual_count = forms.CharField(widget=forms.HiddenInput())
    extra_job_count = forms.CharField(widget=forms.HiddenInput())
    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extraskills', 0)
        extra_language = kwargs.pop('extralang', 0)
        extra_hobby = kwargs.pop('extrahobby', 0)
        extra_qual = kwargs.pop('extraqual', 0)
        extra_job = kwargs.pop('extrajob', 0)
        super(CvCreationForm, self).__init__(*args, **kwargs)
        self.fields['extra_field_count'].initial = extra_fields
        self.fields['extra_language_count'].initial = extra_language
        self.fields['extra_hobby_count'].initial = extra_hobby
        self.fields['extra_qual_count'].initial = extra_qual
        self.fields['extra_job_count'].initial = extra_job
        for index in range(int(extra_fields)):
            # generate extra fields in the number specified via extra_fields
            self.fields['extra_charfield_{index}'.format(index=index+1)] = forms.CharField(label='Skill', required=False)
            self.fields['extra_intfield_{index}'.format(index=index+1)] =  forms.IntegerField(label='Expertise (1-10)', validators=[MaxValueValidator(10), MinValueValidator(1)], required=False)
        for index in range(int(extra_language)):
            self.fields['extra_charfield_lang_{index}'.format(index=index+1)] = forms.CharField(label='Language', required=False)
            self.fields['extra_intfield_lang_{index}'.format(index=index+1)] =  forms.IntegerField(label='Expertise (1-10)', validators=[MaxValueValidator(10), MinValueValidator(1)], required=False)
        for index in range(int(extra_hobby)):
            self.fields['extra_charfield_hobby_{index}'.format(index=index+1)] = forms.CharField(label='Hobby', required=False)
            self.fields['extra_intfield_hobby_{index}'.format(index=index+1)] =  forms.IntegerField(label='Interest (1-10)', validators=[MaxValueValidator(10), MinValueValidator(1)], required=False)
        for index in range(int(extra_qual)):
            self.fields['extra_charfield_qual_{index}'.format(index=index+1)] = forms.CharField(label='Qualification', required=False)
            self.fields['extra_intfield_qual_{index}'.format(index=index+1)] =  forms.CharField(label='Grade', required=False)
        for index in range(int(extra_job)):
            self.fields['extra_charfield_job_{index}'.format(index=index+1)] = forms.CharField(label='Company', required=False)
            self.fields['extra_intfield_job_{index}'.format(index=index+1)] =  forms.CharField(label='Position', required=False)
            self.fields['extra_lenfield_job_{index}'.format(index=index+1)] =  forms.IntegerField(label='Length of employment in months', required=False)

class TestForm(forms.Form):
    extra_question_count = forms.CharField(widget=forms.HiddenInput())
    def __init__(self, *args, **kwargs):
        extra_questions = kwargs.pop('extraquestion', 0)
        extra_names = kwargs.pop('extranames', [])
        super(TestForm, self).__init__(*args, **kwargs)
        self.fields['extra_question_count'].initial = extra_questions
        for index in range(int(extra_questions)):
            # generate extra fields in the number specified via extra_fields
            self.fields['extra_questionfield_{index}'.format(index=index)] = forms.CharField(label='Question '+str(index+1) + ' ' + extra_names[index], required=False)
