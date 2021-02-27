from django.shortcuts import render
from .models import Answer, Quiz, Question
import requests
import os
import cv2
import time
from PIL import Image as PILImage
from PIL import Image
from io import BytesIO
from pathlib import Path
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def test_view(request):
    q1 = Answer.objects.all()
    region = "centralindia" 
    api_key = "cc02edee73f140d38d17232da9899d20"
    path_to_file = "."+q1[0].image.url
    p  = cv2.imread(path_to_file)
    cropped_image = PILImage.fromarray(p)
    buffer = BytesIO()
    cropped_image.save(buffer, format="JPEG")
    image_bytes = buffer.getvalue()
    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = api_key
    headers['Content-Type'] = 'application/octet-stream'
    params = {'language':'en', 'pages':'1','readingOrder':'basic'}
    response = requests.post(
            "https://centralindia.api.cognitive.microsoft.com/vision/v3.2-preview.2/read/analyze?language=en&pages=1&readingOrder=basic",
            headers=headers,
            data=image_bytes,
        )
    headers1 = dict()
    headers1['Ocp-Apim-Subscription-Key'] = api_key
    headers1['Content-Type'] = 'application/json'
    time.sleep(2)
    # urltest = "https://centralindia.api.cognitive.microsoft.com/vision/v3.2-preview.2/read/analyzeResults/"+imageId+"/"
    response1 = requests.request('get',response.headers['Operation-Location'], headers=headers1)
    # # response1 = requests.request('post',"https://{centralindia}.api.cognitive.microsoft.com/vision/v3.2-preview.2/read/analyzeResults/"+imageId)
    # response1_data = response1.json()
    # contxt = {'response':response, 'response1':response1, 'response1_data':response1_data,'imageId':imageId,'urltest':urltest}
    # #call to https://centralindia.api.cognitive.microsoft.com/vision/v3.2-preview.2/read/analyzeResults/imageId(string)
    response1_json = response1.json()
    st = ""
    for i in response1_json["analyzeResult"]["readResults"]:
        for j in i["lines"]:
            st += j["text"]
            st+=' '
    #contxt = {'st':st}
    li = st.split(' ')
    li2 = []
    for i in li:
        li2.append(i.strip(".,!? ").lower())
    print (li2)
    contxt = {'li':li}
    return render(request, 'test.html',contxt)

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
        if request.user.is_teacher==0:
            pk = request.user.username
            return redirect('dashboard_student',pk = pk)
        else:
            pk = request.user.username
            return redirect('dashboard_teacher',pk = pk)
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                pk = request.user.username
                if request.user.is_teacher==0:
                    pk = request.user.username
                    return redirect('dashboard_student',pk = pk)
                else:
                    pk = request.user.username
                    return redirect('dashboard_teacher',pk = pk)
            else:
                messages.info(request, 'Username OR password is incorrect')
        form = LoginForm()
        return render(request, 'login.html', {"form":form})

def dashboard_student(request,pk):
    q1 = Quiz.objects.all()
    context = {'q1':q1}
    return render(request, 'dashboard.html',context)


def Addquestion(request, pk):
    form = QuestionForm()
    print("*******************************************8",pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            qt = form.cleaned_data.get('ques_text')
            kw = form.cleaned_data.get('keywords')
            tm = form.cleaned_data.get('total_marks')
            # user = CustomUser.objects.create_user(username=user1,email= mail,password=passw, is_teacher=0)
            # user.save()
            quiz_obj = Quiz.objects.get(quiz_name=pk)
            quest = Question.objects.create(ques_text=qt, keywords=kw, total_marks=tm, quiz=quiz_obj)
            quest.save()
            messages.success(request, 'Question was created for ' + request.user.username)
            context = {'form':form}
            return redirect('addquestion', pk=pk)
        

    context = {'form':form}
    return render(request, 'addquestion.html', context)


def dashboard_student(request,pk):
    q1 = Quiz.objects.all()
    context = {'q1':q1}
    return render(request, 'dashboard.html',context)
    
def dashboard_teacher(request,pk):
    teacher_obj = Teacher.objects.get(username = request.user.username)
    q1 = Quiz.objects.filter(teacher = teacher_obj)
    context = {'q1':q1, "pk": pk}
    return render(request, 'dash_teacher.html',context)


def Addquiz(request, pk):
    if request.method == 'POST':
        quiz_name = request.POST.get("quizname")
        print("*****************************************", quiz_name)
        t = Teacher.objects.get(username = pk)
        q = Quiz(quiz_name = quiz_name, teacher = t)
        q.save()
        return redirect("dashboard_teacher", pk=pk)
    else:
        return redirect("dashboard_teacher", pk=pk)
def quiz_start(request,pk1,pk2):

    quiz1 = Quiz.objects.filter(quiz_name=pk2)
    quiz = quiz1[0]
    questions = Question.objects.filter(quiz=quiz)
    id_arr = []
    for i in questions:
        id_arr.append(i.ques_id)

    id_arr.sort()
    pk3 = id_arr[0]
    return redirect('quiz_questions', pk1=pk1, pk2=pk2, pk3=pk3)

def quiz_questions(request,pk1,pk2,pk3):
    quiz = Quiz.objects.filter(quiz_name=pk2)[0]
    questions = Question.objects.filter(quiz=quiz)
    id_arr = []
    for i in questions:
        id_arr.append(i.ques_id)

    id_arr.sort()

    ans_arr = []
    stud = Student.objects.get(username=pk1)
    ans = Answer.objects.filter(student=stud)
    for i in ans:
        ans_arr.append(i.question)

    if request.method =="POST":
        if pk3 in ans_arr:
            messages.info(request, "You have already submitted this answer!")
        else:
            #Save image PILLOW
            messages.info(request, "Answer submitted successfully")

        return redirect(quiz_questions,pk1=pk1,pk2=pk2,pk3=pk3)
    params = {"arr":id_arr}
    return render(request,"questions.html",params)
        
        
