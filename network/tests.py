from django.test import TestCase
from .models import *
from django.test import Client


# Create your tests here.
class test_model(TestCase):
    # def setUpTestData(slf):
    #     pass
    """ Test for user model"""
    def setUp(self):
        a = User.objects.create(username="Aaron", email="user@domain.com")
        b = User.objects.create(username="Peter", email="Peter@domain.com")
        c = User.objects.create(username="Peteru", email="Peter@domain.com")

    def test_index(self):
        """ Test for login route"""
        c = Client()
        response = c.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_user(self):
        a = User.objects.get(username="Aaron")
        self.assertEqual(a.username, "Aaron")
    
    def test_user2(self):
        b = User.objects.get(username="Peter")
        self.assertTrue(b.id, 2)

    def test_peter_count(self):
        p = User.objects.all()
        self.assertEqual(p.count(), 3)
