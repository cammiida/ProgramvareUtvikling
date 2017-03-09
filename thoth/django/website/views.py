from django.shortcuts import render
from django.http import HttpResponse
from . import forms

# Create your views here.

def index (request):
    return render(request,'index.html')

def student(request):
    return render(request,'student.html')

def teacher(request):
    return render(request,'teacher.html')

def questions(request):
    if request.method == 'POST':
        form = Questions(request.POST)
        if form.is_valid():

            form.save()
            # redirect
            return render(request, 'questions.html')
        else:
            return HttpResponse("Form Not Valid")
    else:
        form = RecipeForm()

        context = Context({'form': form, })
        context.update(csrf(request))
        template = loader.get_template('myApp/add.html')
        return HttpResponse(template.render(context))