from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django import forms
from .models import *

class Userform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
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
        db_table = 'website_question'
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

class LoginForm(forms.Form):
    username = forms.CharField(max_length=25, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['answer']
