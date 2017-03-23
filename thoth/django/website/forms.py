from django.contrib.auth.models import User
from django import forms
from .models import *

class Userform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    # Info om klassen
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question']

class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['name']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['description','textanswer','option1','option2','option3',
        'option4','option1_correct','option2_correct','option3_correct',
        'option4_correct','timeout']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['answer']