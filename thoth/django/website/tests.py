from django.test import TestCase
import sys
import datetime
from django.utils import timezone
from django.urls import reverse
from .models import *
from django.contrib.auth.models import User
sys.path.insert(0, '/Users/hakongrov/Documents/INDØK/2.År/2.Semester/Programvareutvikling/GIT/ProgramvareUtviklingGroup50/thoth/django')
import API2 as apis

# (resp.status_code, 200) MEANS THINGS ARE OK
# self.assertRedirects(response,'url') CHECKS REDIRECT


class ThothViewsTestCase(TestCase):
    def test_index(self):
        response = self.client.get('/student/')
        self.assertEqual(response.status_code, 200)

class CourseTest(TestCase):
    #All the test for the Course Pages!

    def setUp(self):
        # PROBLEM HERE: THIS REQUIRES LOGIN TO BE TESTED.
        # Solution: create fake login.
        self.user = User.objects.create_user(username='testuser',email=None,password='testpassword')
        self.client.login(username='testuser',password='testpassword')


    #Test that the page opens itself correctly
    def test_addcourse(self):
        response = self.client.get(reverse('addcourse'))
        self.assertEqual(response.status_code, 200)

    def test_addcourseform(self):
        # "POST" Data to the view:
        dict = {'name':'TDT4140'}
        response = self.client.post(reverse('addcourse'),dict)
        self.assertRedirects(response,reverse('courses'))

        # Check that this post now exists in db:
        course = Course.objects.get(id=1)
        self.assertEqual(course.name,'TDT4140')
        # WOO FOUND AN ERROR! AND FIXED IT.

    def test_coursespage(self):
        #add a course to db
        course = Course.objects.create(name='TDT4140',teacher=self.user)
        response = self.client.get(reverse('courses'))
        self.assertEqual(response.status_code, 200)
        #NOW let us test if the redirect page contains the newly created entry
        self.assertContains(response,'TDT4140')

        
        
class QuestionTest(TestCase):
    def setUp(self):
        # PROBLEM HERE: THIS REQUIRES LOGIN TO BE TESTED.
        # Solution: create fake login.
        self.user = User.objects.create_user(username='testuser',email=None,password='testpassword')
        self.client.login(username='testuser',password='testpassword')
    

    def test_add_question(self):
        # Making course and lecture objects since it is needed to create a question
        test_course = Course(name="TDT4140", teacher=self.user, id=1)
        test_lecture = Lecture(name="test_lect", course=test_course, date=timezone.now())
        # Save the objects to the database since when accessing questions it has to be from a lecture
        test_course.save()
        test_lecture.save()
        # Send a post reponse with a question to the add_question page. 
        response = self.client.post('/student/add_question/1/', {"question": "How to use merge sort?"})
        # Testing to see if the reponse code is correct. Should be 302 for redirect
        self.assertEqual(response.status_code, 302)
        # Since we have sent a request to the add_question view it should have made some objects in the API database. Trying to access these.
        a = Api.objects.get(entity_type="Algorithm")
        # Testing to see if it added the correct entity to the database. This is just one of many. 
        self.assertEqual(a.entity_word, "merge sort")
        