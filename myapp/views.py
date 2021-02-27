from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

# def RegisterStudent(request):
 
#     if request.method == "POST":
#         form1 = RegisterForm(request.POST, prefix="form1")
#         form2 = StudentForm(request.POST, prefix="form2")
#         if form1.is_valid():
#             form.save()

#             #return redirect("")
#     else:
#         form1 = RegisterForm()
#         form2 = StudentForm()

#     return render(request, "registerStudent.html", {"form1":form1, "form2":form2})

def RegisterTeacher(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = TeacherForm()
        if request.method == 'POST':
            form = TeacherForm(request.POST)
            if form.is_valid():
                
                user1 = form.cleaned_data.get('username')
                passw = form.cleaned_data.get('password')
                mail = form.cleaned_data.get('email')
                user = CustomUser.objects.create_user(username=user1,email= mail,password=passw, is_teacher=1)
                user.save()
                form.save()
                messages.success(request, 'Account was created for ' + user1)
                return redirect('login')
            

        context = {'form':form}
        return render(request, 'registerTeacher.html', context)

def RegisterStudent(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = StudentForm()
        if request.method == 'POST':
            form = StudentForm(request.POST)
            if form.is_valid():
                
                user1 = form.cleaned_data.get('username')
                passw = form.cleaned_data.get('password')
                mail = form.cleaned_data.get('email')
                user = CustomUser.objects.create_user(username=user1,email= mail,password=passw, is_teacher=0)
                user.save()
                form.save()
                messages.success(request, 'Account was created for ' + user1)
                return redirect('login')
            

        context = {'form':form}
        return render(request, 'registerStudent.html', context)

def index(request):
    return render(request, 'index.html')

def signin(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Username OR password is incorrect')
        form = LoginForm()
        return render(request, 'login.html', {"form":form})
    return render (request, 'login.html')