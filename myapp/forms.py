from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from .models import *


# class RegisterForm(UserCreationForm):
#     #email = forms.EmailField()

#     class Meta:
#         model = CustomUser
#         fields = ["username", "password", "email"]

class RegisterForm(forms.Form):
    username = forms.CharField(label = 'Username', max_length = 12)
    password = forms.CharField(label = 'Password',min_length = 6, widget = forms.PasswordInput())
    email = forms.CharField(label = 'email', max_length = 20)


class StudentForm(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = ["username", "password", "email", "name"]
        widgets = {'password' : forms.PasswordInput()}

class TeacherForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = ["username", "password", "email", "subject", "name"]
        widgets = {'password' : forms.PasswordInput()}

class LoginForm(forms.Form):
    username = forms.CharField(label = 'Username', max_length = 12)
    password = forms.CharField(label = 'Password',min_length = 6, widget = forms.PasswordInput())

class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ["image",]
