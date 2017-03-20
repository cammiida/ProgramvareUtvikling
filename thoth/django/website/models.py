from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=200, unique=True)
    teacher = models.ForeignKey(User)

    def __str__(self):
        return self.name

class Lecture(models.Model):
    course = models.ForeignKey(Course)
    date = models.DateTimeField(auto_now = True)
    name = models.CharField(max_length=200)
    active = models.BooleanField(default = False)

    def __str__(self):
        return self.date.strftime("%B %d, %Y")


class Task(models.Model):
    lecture = models.ForeignKey(Lecture)
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
    quesiton = models.CharField(max_length=500)
    value = models.PositiveIntegerField(default=0)
    answer = models.CharField(default=None, max_length=200)
    lecture = models.ForeignKey(Lecture)

    def __str__(self):
        return self.quesiton
