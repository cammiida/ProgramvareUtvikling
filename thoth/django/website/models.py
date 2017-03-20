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
    active = models.BooleanField(default = False)

    def __str__(self):
        return self.date.strftime("%B %d, %Y")

class Questions(models.Model):
    question = models.CharField(max_length=500)
    value = models.PositiveIntegerField(default=0)
    answer = models.CharField(max_length=500, default="")
    #lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)

    def __str__(self):
        return self.question + self.answer

