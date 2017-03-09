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
    active = models.BooleanField(default = False)

    def __str__(self):
        return self.date.strftime("%B %d, %Y")
