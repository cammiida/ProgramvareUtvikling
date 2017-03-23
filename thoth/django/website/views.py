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
    #return render(request,'student/question_list.html')
    return render(request, 'student/index.html')

def studentlecture(request):
    lecture = Lecture.objects.get(id=request.GET['lectureid'])
    all_questions = Question.objects.filter(lecture=lecture)
    form = QuestionForm()
    return render(request, 'student/lecture.html', {'lecture':lecture, 'all_questions':all_questions, 'form':form})

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
    lectures = Lecture.objects.filter(course=course_id,course__teacher=request.user).order_by('-id')
    all_questions = Question.objects.filter(lecture__course=course_id)

    return render(request, 'teacher/lectures.html', {'lectures':lectures,'course':course, 'all_questions':all_questions})

def lecture(request,lecture_id):
    lecture = Lecture.objects.get(id=lecture_id)
    tasks = Task.objects.filter(lecture = lecture)
    #lectures = Lecture.objects.filter(course=course_id,course__teacher=request.user).order_by('-id')
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # add course from form, but dont add it to db just yet.
            task = form.save(commit=False)
            # Now add current user to the course
            task.lecture_id = lecture_id
            # now add it to db since we now have all our stuffs
            task.save()

            return redirect('lecture', lecture_id)
    else:
        form = TaskForm()
    return render(request, 'teacher/lecture.html', {'lecture':lecture, 'form':form, 'tasks':tasks})

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

def startlecture(request, lecture_id):
    lectures = Lecture.objects.filter(course__teacher = request.user)
    for lecture in lectures:
        lecture.active = False
        lecture.save()
    lecture = Lecture.objects.get(id=lecture_id)
    lecture.active = True
    lecture.save()
    return redirect('activelecture')

def addlecture(request, course_id):
    # checks if the form is posted. If it is, create the object
    course = Course.objects.get(id=course_id)
    if request.method == 'POST':
        form = LectureForm(request.POST)
        if form.is_valid():
            lecture = form.save(commit=False)
            lecture.course_id = course_id
            lecture.save()
            return redirect('lectures',course_id)
    else:
        form = LectureForm()
    return render(request,'teacher/addlecture.html',{'form':form, 'course':course})




def activelecture(request):
    lecture = Lecture.objects.get(active=True,course__teacher = request.user)
    tasks = Task.objects.filter(lecture = lecture)
    return render(request,'teacher/activelecture.html',{'lecture':lecture, 'tasks':tasks})

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



def add_question(request,lectureid):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            addquestion = form.save(commit=False)
            addquestion.lecture_id = lectureid
            addquestion.save()
            return redirect('/student/lecture/?lectureid=' + str(lectureid))
    else:
        form = QuestionForm()
    return render(request, 'student/add_question.html', {'form': form})


def question_list(request):
    all_questions = Question.objects.all()
    template = 'student/question_list.html'
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

def answer_question(request, question_id):
    question = Question.objects.get(id = question_id)
    lecture = question.lecture

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=question)
        if form.is_valid():
            answer_question = form.save(commit=False)
            answer_question.lecture_id = lecture.id
            answer_question.save()
            return render(request, 'teacher/answer_question.html', {'question': question, 'lecture':lecture, 'form':form})
    else:
        form = AnswerForm(instance=question)
        return render(request, 'teacher/answer_question.html', {'question': question, 'lecture': lecture, 'form': form})