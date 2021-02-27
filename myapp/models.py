from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    is_teacher = models.BooleanField(default = 1)

class Teacher(models.Model):
    username = models.CharField(unique=True, max_length = 30)
    password = models.CharField(max_length = 30)
    email = models.CharField(max_length = 30)
    subject = models.CharField(max_length = 30)
    name = models.CharField(max_length = 30)

    def __str__(self):
        return self.name

class Student(models.Model):
    username = models.CharField(unique=True, max_length = 30)
    password = models.CharField(max_length = 30)
    email = models.CharField(max_length = 30, null = True)
    name = models.CharField(max_length = 30)

    def __str__(self):
        return self.name

class Quiz(models.Model):
    quiz_id = models.AutoField(primary_key = True)
    teacher = models.ForeignKey(Teacher, on_delete = models.CASCADE)
    student = models.ForeignKey(Student, on_delete = models.CASCADE, null=True)

    def __str__(self):
        return self.quiz_id

class Question(models.Model):
    ques_text = models.TextField()
    keywords = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete = models.CASCADE)

class Answer(models.Model):
    # student = models.ForeigKey(student)
    image = models.ImageField(upload_to='myapp/uploads/')
    ans_text = models.TextField(null = True)
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    student = models.ForeignKey(Student, on_delete = models.CASCADE, null = True)
    grade = models.DecimalField(max_digits=3, decimal_places=0, null=True)

