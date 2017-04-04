from django.test import TestCase
from django.urls import reverse
from .models import *
from django.contrib.auth.models import User

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
