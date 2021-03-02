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
from django.core.files.storage import FileSystemStorage
import decimal
def grade_file(s):
    # q1 = Answer.objects.all()
    region = "centralindia" 
    api_key = "cc02edee73f140d38d17232da9899d20"
    # path_to_file = "."+q1[0].image.url
    path_to_file = "./myapp/uploads"+s
    # print(path_to_file,'###################')
    p  = cv2.imread(path_to_file)
    # print(p,'Image')
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
    return li2
    # return render(request, 'test.html',contxt)

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
            # return redirect('dashboard_student',pk = pk)
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

def signout(request):
	logout(request)
	return redirect('login')


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
    context = {'q1':q1, "pk":pk}
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
# def quiz_start(request,pk1,pk2, pk3):

#     try: 
#         quiz1 = Quiz.objects.filter(quiz_name=pk2)
#         quiz = quiz1[0]
#         questions = Question.objects.filter(quiz=quiz)
#         id_arr = []
#         for i in questions:
#             id_arr.append(i.ques_id)

#         id_arr.sort()
#         pk3 = id_arr[0]
#         return redirect('quiz_questions', pk1=pk1, pk2=pk2, pk3=pk3)

#     except: 
#         return redirect('quiz_questions', pk1=pk1, pk2=pk2, pk3=pk3)
def result(request,pk1,pk2):
    #pk1 = username
    #pk2 = quiz_name
    tot_grade = 0
    quizq = Quiz.objects.get(quiz_name = pk2)
    studentobj = Student.objects.get(username = pk1)
    if quizq:
        quesq = Question.objects.filter(quiz = quizq)
        for i in quesq:  
            ansq = Answer.objects.filter(question = i, student = studentobj )
            if ansq:
                tot_grade+=ansq[0].grade
    context = {'tot_grade':tot_grade, 'pk2': pk2, 'pk1':pk1}
    #att = Quiz_Attempted(quiz = quizq, student = studentobj, tot_grade = tot_grade)
    #aatt.save()

    return render(request, 'result.html',context)
    # return render(request, 'dashboard.html',context)

def quiz_start(request,pk1,pk2):

    quiz1 = Quiz.objects.filter(quiz_name=pk2)
    quiz = quiz1.first()
    questions = Question.objects.filter(quiz=quiz)
    id_arr = []
    for i in questions:
        id_arr.append(i.ques_id)

    id_arr.sort()
    if len(id_arr)==0:
        return redirect('dashboard_student', pk1)
    pk3 = id_arr[0]
    return redirect('quiz_questions', pk1=pk1, pk2=pk2, pk3=pk3)

def quiz_questions(request,pk1,pk2,pk3):
    quiz = Quiz.objects.filter(quiz_name=pk2).first()
    questions = Question.objects.filter(quiz=quiz)
    ques = Question.objects.get(ques_id=pk3)
    id_arr = []
    for i in questions:
        id_arr.append(i.ques_id)

    id_arr.sort()

    ans_arr = []
    stud = Student.objects.get(username=pk1)
    ans = Answer.objects.filter(student=stud)
    for i in ans:
        ans_arr.append(i.question)
    form = AnswerForm()
    if request.method =="POST":
        if pk3 in ans_arr:
            messages.info(request, "You have already submitted this answer!")
        else:
            if request.FILES['myfile']:
                myfile = request.FILES['myfile']
                fs = FileSystemStorage(location = 'myapp/uploads/')
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)
                l1 = grade_file(uploaded_file_url)
                #li is list of detected words
                quesquer = Question.objects.get(ques_id = pk3)
                keywords = quesquer.keywords.split()
                ctr  = len(keywords)
                ctr1=0
                for i in keywords:
                    if i.lower() in l1:
                        ctr1=ctr1+1
                grade1 = 0.0
                # print(ctr1,'^^^^^^')
                # print(ctr,'THis is ctr')
                if ctr1>=0.8*ctr:
                    grade1 = quesquer.total_marks
                elif ctr1>=0.6*ctr:
                    grade1 = quesquer.total_marks*decimal.Decimal(0.8)
                elif ctr1>=0.4*ctr:
                    grade1 = quesquer.total_marks*decimal.Decimal(0.6)
                elif ctr1>=0.2*ctr:
                    grade1 = quesquer.total_marks*decimal.Decimal(0.4)
                str1 = ' '
                studobj = Student.objects.get(username = pk1)
                a = Answer.objects.create(ans_text = str1.join(l1), question = quesquer, student = studobj, grade = grade1)
                # print(uploaded_file_url)
                # print(filename)
            #Save image PILLOW
            messages.info(request, "Answer submitted successfully")

        return redirect(quiz_questions,pk1=pk1,pk2=pk2,pk3=pk3)
    params = {"arr":id_arr,"form":form,'pk1':pk1,'pk2':pk2,'pk3':pk3,"ques":ques}
    return render(request,"questions.html",params)
        
        
def home(request):
    return render(request, 'home.html')
    