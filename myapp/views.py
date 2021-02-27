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
import os
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