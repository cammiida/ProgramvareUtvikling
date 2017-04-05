from django.db import models
#from django.core.urlresolvers import reverse
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=200, unique=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now = True)
    name = models.CharField(max_length=200)
    active = models.BooleanField(default = False)

    def __str__(self):
        return self.date.strftime("%B %d, %Y")


class Task(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    textanswer = models.CharField(max_length=500, blank=True)
    option1 = models.CharField(max_length=500, blank=True)
    option2 = models.CharField(max_length=500, blank=True)
    option3 = models.CharField(max_length=500, blank=True)
    option4 = models.CharField(max_length=500, blank=True)
    option1_correct = models.BooleanField(default=False)
    option2_correct = models.BooleanField(default=False)
    option3_correct = models.BooleanField(default=False)
    option4_correct = models.BooleanField(default=False)
    timeout = models.PositiveIntegerField()
    def __str__(self):
        return self.description

class Question(models.Model):
    question = models.CharField(max_length=500)
    value = models.IntegerField(default=0)
    answer = models.CharField(max_length=500, default="", blank=True)
    api_answer = models.CharField(max_length=500, default="", blank=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.question

class Api(models.Model):
    entity_type = models.CharField(max_length=30)
    entity_word = models.CharField(max_length=30)
    answer_set = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    def __str__(self):
        return (self.question.question)
