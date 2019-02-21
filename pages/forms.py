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

    class Meta:
        model = AppUser
        fields = ['email', 'password']


class LoginUserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), max_length=50)

    class Meta:
        model = AppUser
        fields = ['email', 'password']

class CvCreationForm(forms.Form):
    name = forms.CharField(label='Name', max_length=50, required=False)
    extra_field_count = forms.CharField(widget=forms.HiddenInput())
    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra', 0)

        super(CvCreationForm, self).__init__(*args, **kwargs)
        self.fields['extra_field_count'].initial = extra_fields

        for index in range(int(extra_fields)):
            # generate extra fields in the number specified via extra_fields
            self.fields['extra_charfield_{index}'.format(index=index)] = forms.CharField(label='Skill', required=False)
            self.fields['extra_intfield_{index}'.format(index=index)] =  forms.IntegerField(label='Expertise (1-10)', validators=[MaxValueValidator(10), MinValueValidator(1)], required=False)
