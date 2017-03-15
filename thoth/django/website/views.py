from django.shortcuts import render
from django.http import HttpResponse
from .models import Question

# Create your views here.

def index (request):
    return render(request,'index.html')

def student(request):
    return render(request,'student.html')

def teacher(request):
    return render(request,'teacher.html')

def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():

            form.save()
            # redirect


            return render(request,'questions.html')
        else:
            return HttpResponse("Form Not Valid")

    return render(request, 'website/question.html', {'obj': models.Question.objects.all()})


def question(request):
    return render