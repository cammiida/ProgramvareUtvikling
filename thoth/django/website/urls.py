"""thoth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    #r'^/*$'
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^teacher/about/$', views.about_teacher, name='about_teacher'),
    url(r'^savetaskhistory/$', views.savetaskhistory),
    url(r'^taskhistory/([0-9]+)?$', views.taskhistory, name='taskhistory'),
    url(r'^savefeedback/$', views.savefeedback),
    url(r'^feedbackhistory/([0-9]+)?$', views.feedbackhistory, name='feedbackhistory'),

    #student urls
    url(r'^student/$', views.student, name='student'),
    url(r'^student/lecture/([0-9]+)?$', views.studentlecture, name='studentlecture'),
    url(r'^student/add_question/([0-9]+)/$', views.add_question, name='add_question'),
    url(r'^student/question_list/([0-9]+)/$', views.question_list, name='question_list'),

    #voting a question up or down
    url(r'^student/lecture/vote/(?P<question_id>[0-9]+)$', views.vote, name='vote'),


    #teacher urls
    url(r'^teacher/$', views.teacher, name='teacher'),
    url(r'^login/$', views.login1, name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),
    #url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^lecturespeed/$', views.lecturespeed, name='lecturespeed'),
    url(r'^addcourse/$', views.addcourse, name='addcourse'),
    url(r'^addlecture/([0-9]+)/$', views.addlecture, name='addlecture'),
    url(r'^startlecture/([0-9]+)/$', views.startlecture, name='startlecture'),
    url(r'^lecture/([0-9]+)/$', views.lecture, name='lecture'),
    url(r'^courses/$', views.courses, name='courses'),
    url(r'^activelecture/$', views.activelecture, name='activelecture'),
    url(r'^endlecture/$', views.endlecture, name='endlecture'),
    url(r'^lectures/([0-9]+)/$', views.lectures, name='lectures'),
    url(r'^registration/$', views.register, name='register'),
    url(r'^teacher/answer_question/(?P<question_id>[0-9]+)/$', views.answer_question, name='answer_question'),
    url(r'^teacher/delete_answer_question/(?P<question_id>[0-9]+)/$', views.delete_answer_question, name='delete_answer_question'),

]
