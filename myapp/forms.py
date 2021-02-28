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
    password = forms.CharField(label = 'Password',min_length = 6, widget = forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: 75%;'}))
    email = forms.CharField(label = 'email', max_length = 20)


class StudentForm(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = ["username", "password", "email", "name"]
        widgets = {
            'password' : forms.PasswordInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'})
            }

class TeacherForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = ["username", "password", "email", "subject", "name"]
        widgets = {
            'password' : forms.PasswordInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'})
            }

class LoginForm(forms.Form):
    username = forms.CharField(label = 'Username', max_length = 12, widget = forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label = 'Password',min_length = 6, widget = forms.PasswordInput(attrs={'class': 'form-control'}))

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["ques_text", "keywords", "total_marks"]
        widgets = {
            'ques_text' : forms.TextInput(attrs={'class': 'form-control'}),
            'keywords': forms.TextInput(attrs={'class': 'form-control'}),
            'total_marks': forms.TextInput(attrs={'class': 'form-control'}),
            }
    username = forms.CharField(label = 'Username', max_length = 12)
    password = forms.CharField(label = 'Password',min_length = 6, widget = forms.PasswordInput())

class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ["image",]
