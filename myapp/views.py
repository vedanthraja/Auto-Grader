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

# Create your views here.
# def test_view(request):
#     q1 = Answer.objects.all()
#     region = "centralindia" 
#     api_key = "cc02edee73f140d38d17232da9899d20"
#     path_to_file = r"E:\Hackathons\Auto-Grader\uploads\img1.png"
#     headers = {
#     "Ocp-Apim-Subscription-Key": api_key,
#     'Content-Type': 'application/octet-stream'}
#     p = cv2.imread(path_to_file)
#     cropped_image = PILImage.fromarray(p)
#     buffer = BytesIO()
#     cropped_image.save(buffer, format="JPEG")
#     image_bytes = buffer.getvalue()



def test_view(request):
    q1 = Answer.objects.all()
    region = "centralindia" 
    api_key = "cc02edee73f140d38d17232da9899d20"
    # path_to_file = request.build_absolute_uri(q1[0].image.url)
    # path_to_file = r"\uploads\sample.jpeg"  #This is the correct one
    # BASE_DIR = Path(__file__).resolve().parent.parent
    # BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    # path_to_file1 = BASE_DIR.join(q1[0].image.url)
    # print(path_to_file1)
    # Read file
    path_to_file = "."+q1[0].image.url
    p  = cv2.imread(path_to_file)
    cropped_image = PILImage.fromarray(p)
    buffer = BytesIO()
    cropped_image.save(buffer, format="JPEG")
    image_bytes = buffer.getvalue()
    # with open(path_to_file, 'rb') as f:
    #     data = f.read()

    # Set request headers
    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = api_key
    headers['Content-Type'] = 'application/octet-stream'

    # Set request querystring parameters
    # params = {'visualFeatures': 'Color,Categories,Tags,Description,ImageType,Faces,Adult'}
    params = {'language':'en', 'pages':'1','readingOrder':'basic'}
    #https://centralindia.api.cognitive.microsoft.com/vision/v3.2-preview.2/read/analyzeResults/7aec5573-e709-4203-a329-465d83da1a8d
    # Make request and process response
    response = requests.post(
            "https://centralindia.api.cognitive.microsoft.com/vision/v3.2-preview.2/read/analyze?language=en&pages=1&readingOrder=basic",
            headers=headers,
            data=image_bytes,
        )
    # response = requests.request('post', "https://{}.api.cognitive.microsoft.com/vision/v1.0/analyze".format(region), data=image_bytes, headers=headers, params = params)
    # contxt = {'resp':response}
    # response_data = response.json()
    # print(response.headers)
    # imageId = response_data["requestId"]
    # params1 = {'operationId':imageId,}
    headers1 = dict()
    headers1['Ocp-Apim-Subscription-Key'] = api_key
    headers1['Content-Type'] = 'application/json'
    # # contxt = {'imgId':imageId}
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
        if request.user.is_teacher==0:
            pk = request.user.username
            return redirect('dashboard_student',pk = pk)
        # else:
        #     pk = request.user.username
        #     return redirect('dashboard_student',pk = pk)
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                pk = request.user.username
                return redirect('dashboard_student',pk = pk)
            else:
                messages.info(request, 'Username OR password is incorrect')
        form = LoginForm()
        return render(request, 'login.html', {"form":form})

def dashboard_student(request,pk):
    q1 = Quiz.objects.all()
    context = {'q1':q1}
    return render(request, 'dashboard.html',context)