from .models import *
from .forms import *

# Create your views here.
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
#from django.core.urlresolvers import reverse_lazy
from django.urls import reverse_lazy
from django.views.generic import View
from django.http import HttpResponse
from django.template import loader

def index (request):
    return render(request, 'index.html')

def student(request):
    #return render(request,'student/questions.html')
    return render(request, 'student/index.html')

def studentlecture(request):
    lecture = Lecture.objects.get(id=request.GET['lectureid'])
    return render(request, 'student/lecture.html', {'lecture':lecture})

def teacher(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    return render(request, 'teacher/index.html', {'username': username})

def courses(request):
    courses = Course.objects.filter(teacher=request.user)
    return render(request, 'teacher/courses.html', {'courses':courses})

def lectures(request,course_id):
    course = Course.objects.get(id=course_id)
    lectures = Lecture.objects.filter(course=course_id,course__teacher=request.user)
    return render(request, 'teacher/lectures.html', {'lectures':lectures,'course':course})

def addcourse(request):
    # checks if the form is posted. If it is, create the object
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            # add course from form, but dont add it to db just yet.
            course = form.save(commit=False)
            # Now add current user to the course
            course.teacher = request.user
            # now add it to db since we now have all our stuffs
            course.save()

            return redirect('../courses')
    else:
        form = CourseForm()
    return render(request,'teacher/addcourse.html',{'form':form})

def addlecture(request, course_id):
    lectures = Lecture.objects.filter(course__teacher = request.user)
    for lecture in lectures:
        lecture.active = False
        lecture.save()
    lecture = Lecture()
    lecture.course_id = course_id
    lecture.active = True
    lecture.save()
    return redirect('activelecture')

def activelecture(request):
    lecture = Lecture.objects.get(active=True,course__teacher = request.user)
    return render(request,'teacher/addlecture.html',{'lecture':lecture})

def endlecture(request):
    lecture = Lecture.objects.get(active=True,course__teacher = request.user)
    lecture.active = False
    lecture.save()
    return  redirect('lectures',lecture.course.id)


def lecturespeed(request):
    return render(request, 'teacher/lecturespeed.html')

class UserFormView(View):
    form_class = Userform
    template_name = 'teacher/registration_form.html'
        #Displays blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})
    # legger til bruker i databasen
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            #lager et objekt men lagrer det ikke til databasen, lagrer den lokalt
            user = form.save(commit=False)
            # clean data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #endre passord
            user.set_password(password)
            user.save()
            # returns userobjekt hvis all info er korrekt
            #sjekker om brukernavn og passord er i databasenn
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('teacher')
        return render(request, self.template_name, {'form': form})
#skal egentlig ha render_to_response, men fikk hele tiden error når jeg brukte det,
#skjønner ikke hvorfor

def login1(request):
    message = ""
    if request.method == 'POST':
        username = request.POST['u']
        password = request.POST['p']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('teacher')
            else:
                message = "user is disabled"
    else:
        message = "User doesn't exist"

    return render(request, 'teacher/login.html', {'message':message})

def logout_view(request):
    logout(request)
    return render(request, 'teacher/logout.html')



def add_questions(request):
    form = QuestionForm()
    template = 'student/questions.html'

    if request.method == 'POST':
        form = form(request.POST)
        if form.is_valid():
            question = form.save(commit=False)

            question = form.cleaned_data['question']
            question.save()

            return render(request, template, {{'questionForm':form}})
        else:
            return HttpResponse("Form Not Valid")
    return render(request, 'student/question.html')

def answer_questions(request):
    if request.method == 'POST':
        return

def questions(request):
    all_questions = Question.objects.all()
    template = 'student/questions.html'
    context = {
        'all_questions' : all_questions,

    }
    # KAN KANKSJE BRUKES NÅR LÆRER SKAL KUNNE LEGGE TIL SVAR PÅ SPØRSMÅL

    #html=''
    #for question in all_questions:
    #    url = 'student/questions/' + str(question.id) + '/'
    #    html += '<a href= "' + url + '">' + question.question + '</a><br>'


    #return HttpResponse(template.render(context, request))
    return render(request,template,context)
