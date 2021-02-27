from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.
class Quiz(models.Model):
    quiz_id = models.AutoField(primary_key = True)
    # teacher = models.ForeigKey(teacher)
class Question(models.Model):
    ques_text = models.TextField()
    keywords = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete = models.CASCADE)



class Answer(models.Model):
    # student = models.ForeigKey(student)
    image = models.FileField(upload_to='uploads/')
    ans_text = models.TextField()
    question = models.ForeignKey(Question, on_delete = models.CASCADE)