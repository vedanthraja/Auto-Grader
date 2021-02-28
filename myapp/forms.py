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
    password = forms.CharField(label = 'Password',min_length = 6, widget = forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: 75%;', 'placeholder': 'Add Password'}))
    email = forms.CharField(label = 'email', max_length = 20)


class StudentForm(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = ["username", "password", "email", "name"]
        widgets = {
            'password' : forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Add Password'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add Password'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add Password'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add Password'})
            }

class TeacherForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = ["username", "password", "email", "subject", "name"]
        widgets = {
            'password' : forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Add Password'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add Password'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add Password'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add Password'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add Password'})
            }

class LoginForm(forms.Form):
    username = forms.CharField(label = 'Username', max_length = 12, widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Add Password'}))
    password = forms.CharField(label = 'Password',min_length = 6, widget = forms.PasswordInput(attrs={'class': 'form-control',  'placeholder': 'Add Password'}))

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["ques_text", "keywords", "total_marks"]
        widgets = {
            'ques_text' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add Password'}),
            'keywords': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add Password'}),
            'total_marks': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add Password'}),
            }
    username = forms.CharField(label = 'Username', max_length = 12)
    password = forms.CharField(label = 'Password',min_length = 6, widget = forms.PasswordInput())

class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ["image",]
