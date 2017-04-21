from .models import *
from .forms import *
from django.db import OperationalError
from django.db.models import F
from django.db.models import Q
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
import sys
#sys.path.insert(0, '/Users/hakongrov/Documents/INDØK/2.År/2.Semester/Programvareutvikling/GIT/ProgramvareUtviklingGroup50/thoth/django')
import API2 as apis


def index (request):
    return render(request, 'index.html')

def about_teacher (request):
    return render(request, 'about.html',{'teacher': True})

def about (request):
    return render(request, 'about.html')

def student(request):
    #return render(request,'student/question_list.html')
    return render(request, 'student/index.html', {'not_show_icon': True})

def studentlecture(request, lecture_id):
    try:
        # TODO: use LectureForm fra forms.py
        lecture = Lecture.objects.get(id=request.GET['lectureid'])
    except:
        message =   "You have entered an incorrect ID"
        return render(request, 'student/index.html', {'not_show_icon':True, 'error': message})
    all_questions = Question.objects.filter(lecture=lecture).order_by('value')
    tasks = Task.objects.filter(lecture=lecture)
    form = QuestionForm()
    return render(request, 'student/lecture.html', {'lecture':lecture, 'tasks':tasks, 'all_questions':all_questions, 'form':form})

def teacher(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    return render(request, 'teacher/index.html', {'username': username})

def courses(request):
    courses = Course.objects.filter(teacher=request.user)
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
            return redirect('courses')
    else:
        form = CourseForm()
    return render(request, 'teacher/courses.html', {'courses':courses,'form':form})

def lectures(request,course_id):
    course = Course.objects.get(id=course_id)
    lectures = Lecture.objects.filter(course=course_id,course__teacher=request.user).order_by('-id')
    for lecture in lectures:
        lecture.active = False
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

    return render(request, 'teacher/lectures.html', {'lectures':lectures,'course':course,'form':form})

def lecture(request,lecture_id):
    all_questions = Question.objects.filter(lecture = lecture_id).order_by('-timestamp')
    lecture = Lecture.objects.get(id=lecture_id)
    tasks = Task.objects.filter(lecture = lecture)
    feedbackhistory = FeedbackHistory.objects.filter(lecture = lecture).order_by('timestamp')
    line_chart_array = []
    for entry in feedbackhistory:
        date = entry.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        entry_array = [date, entry.up, entry.down, entry.none]
        line_chart_array.append(entry_array)
    feedbackhistory = FeedbackHistory.objects.filter(lecture=lecture).order_by('-timestamp')
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # add course from form, but dont add it to db just yet.
            task = form.save(commit=False)
            # Now add current user to the course
            task.lecture_id = lecture_id
            # now add it to db since we now have all our stuffs
            task.save()
            print('OK')
            return redirect('lecture', lecture_id)
    else:
        form = TaskForm()
    return render(request, 'teacher/lecture.html', {'lecture':lecture, 'form':form, 'tasks':tasks,
                                                    'all_questions':all_questions, 'feedbackhistory':feedbackhistory,
                                                    'line_chart_array':line_chart_array})

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

            return redirect('courses')
    else:
        form = CourseForm()
    return render(request,'teacher/addcourse.html',{'form':form})

def startlecture(request, lecture_id):
    lectures = Lecture.objects.filter(course__teacher = request.user)
    print(lectures)
    for lecture in lectures:
        lecture.active = False
        lecture.save()
    lecture = Lecture.objects.get(id=lecture_id, course__teacher = request.user)
    lecture.active = True
    lecture.save()
    print('lecture started')
    return redirect('activelecture', lecture.id)

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


def activelecture(request, lecture_id):
    lecture = Lecture.objects.get(id = lecture_id,course__teacher = request.user)
    lecture.active = True
    all_questions = Question.objects.filter(lecture=lecture_id).order_by('-timestamp')
    tasks = Task.objects.filter(lecture = lecture)
    print('This lecture is active')
    return render(request,'teacher/activelecture.html', {'lecture':lecture, 'tasks':tasks, 'all_questions':all_questions})

def savetaskhistory(request):
    if request.method == 'POST':
        print('POSTING STUFF')
        history = TaskHistory()
        history.correct_answers = request.POST['correct']
        history.wrong_answers = request.POST['wrong']
        history.timeout_answers = request.POST['timedoutnr']
        history.task_id = request.POST['taskid']
        history.save()
        print('STUFF POSTED')
    else:
        print('ERROR')
    return HttpResponse('OK')

def savefeedback(request):
    if request.method == 'POST':
        print('POSTING STUFF')
        history = FeedbackHistory()
        history.up = request.POST['up']
        history.down = request.POST['down']
        history.none = request.POST['none']
        history.lecture_id = request.POST['lectureid']
        history.save()
        print('STUFF POSTED')
    else:
        print('ERROR')
    return HttpResponse('OK')

def feedbackhistory(request,lectureid):
    entries = FeedbackHistory.objects.filter(lecture_id=lectureid)
    return render(request,'teacher/taskhistory.html',{
        'entries':entries,
    })

def taskhistory(request,taskid):
    taskentries = TaskHistory.objects.filter(task_id=taskid)
    total_correct_answers = 0
    total_wrong_answers = 0
    total_timeout_answers = 0
    for entry in taskentries:
        total_correct_answers += entry.correct_answers
        total_wrong_answers += entry.wrong_answers
        total_timeout_answers += entry.timeout_answers
    task = Task.objects.get(id=taskid)
    return render(request,'teacher/taskhistory.html',{
        'taskentries':taskentries,
        'task':task,
        'total_correct_answers':total_correct_answers,
        'total_wrong_answers':total_wrong_answers,
        'total_timeout_answers':total_timeout_answers
    })


def endlecture(request):
    lectures = Lecture.objects.filter(course__teacher = request.user)
    #lecture = Lecture.objects.get(active=True,course__teacher = request.user)
    for lecture in lectures:
        print(lecture.active)
        lecture.active = False
        lecture.save()
        print(lecture.active)
    print('lecture ended')
    return redirect('lecture',lecture.id)

def login1(request):
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return redirect("teacher")# Redirect to a success page.
    return render(request, 'teacher/login.html', {'form': form })


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
            form = QuestionForm()
            try:
                apis.predict(addquestion)
                apis.similar(addquestion)
            except:
                pass
    else:
        form = QuestionForm()

    return redirect('/student/lecture/?lectureid=' + str(lectureid), {'form': form})


def question_list(request,lecture_id):
    all_questions = Question.objects.filter(lecture_id=lecture_id).order_by('-timestamp')
    return render(request,'student/question_list.html',{'all_questions' : all_questions})

def register(request):
    registered = False
    if(request.method == 'POST'):
        user_form = Userform(data=request.POST)
        if(user_form.is_valid()):
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print (user_form.errors)
    else:
        user_form = Userform()
    return render(request, 'teacher/registration.html', {'form': user_form, 'registered': registered})


def answer_question(request, question_id):
    questions = Question.objects.filter(id = question_id)
    question = questions.first()
    print(question)
    lecture = question.lecture
    a = Api.objects.all().filter(question__exact = question)
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=question)
        if form.is_valid():
            answer_question = form.save(commit=False)
            answer_question.lecture_id = lecture.id
            apis.update(answer_question.question, answer_question.answer)
            answer_question.save()
            a.update(answer_set=True)
            if lecture.active:
                return redirect('activelecture', lecture.id)
            else:
                return redirect('lecture', lecture.id)
    else:
        form = AnswerForm(instance=question)
        return render(request, 'teacher/answer_question.html', {'question': question, 'lecture': lecture, 'form': form})

def vote(request, question_id):
    print("test")
    question = Question.objects.get(id = question_id)
    lecture = question.lecture
    all_questions = Question.objects.filter(lecture=lecture.id).order_by('value')
    form = QuestionForm()
    if request.POST.get('up_button'):
        print("up")
        question.value = F('value') + 1
        question.save()
    elif request.POST.get('down_button'):
        print("down")
        question.value = F('value') - 1
        questions_less_than = Question.objects.filter(value__lte=-5)
        if questions_less_than:
            questions_less_than.delete()
        else:
            question.save()

    return HttpResponse('OK')
    #return render(request, 'student/lecture.html', {'lecture':lecture, 'all_questions':all_questions, 'form':form})

def delete_answer_question(request, question_id):
    question = Question.objects.get(id = question_id)
    lecture = question.lecture
    all_questions = Question.objects.filter(lecture=lecture.id).order_by('value')
    if request.POST.get('answer_button'):
        form = QuestionForm()
        #if request.method == 'POST':
        return redirect('answer_question', question_id)
    if request.POST.get('delete_button'):
        #if request.method == 'POST':
        question.delete()
        if lecture.active == True:
            return redirect('activelecture', lecture.id)
        else:
            return redirect('lecture', lecture.id)

    return render(request, 'teacher/answer_question.html', {'question': question, 'lecture': lecture, 'form': form})
