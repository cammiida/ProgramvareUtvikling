from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View
from .forms import Userform


# Create your views here.

def index (request):
    return render(request, 'index.html')

def student(request):
    return render(request, 'student/student.html')

def teacher(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    return render(request, 'teacher/index.html', {'username': username})


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

#skal egentlig ha render_to_response, men fikk hele tiden error n�r jeg brukte det, skj�nner ikke hvorfor
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

