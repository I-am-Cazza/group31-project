from django import forms
from django.forms import ModelForm
from app.models import AppUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=20, required=True, help_text="*")
    first_name = forms.CharField(max_length=20, required=True, help_text='*')
    last_name = forms.CharField(max_length=30, required=True, help_text='*')
    email = forms.EmailField(max_length=254, required=True,help_text='*')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


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
