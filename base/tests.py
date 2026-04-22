from base.models import Todo
from django.contrib.auth import get_user_model

from rest_framwork.test import APITestCase
from rest_framework import status
from django.urls import reverse

User = get_user_model()

class TodoAPITestCase(APITestCase):
    def setUp(self):
        #create a test user
        self.user = User.objects.create_user(
            email='testuser@example.com', 
            password='testpassword123',
            first_name='Test',
            last_name='User',
            phone_number='1234567890',
        )

        self.user_data = {
            'email': "newuser@example.com",
            'password': "newpassword123",
            'first_name': "New",
            'last_name': "User",
            'phone_number': "0987654321"
        }

        self.todo = Todo.objects.create(
            user=self.user,
            title="Test Todo",
            description="This is a test todo item.",
            completed=False
        )

        self.todo_data = {
            'title': "New Test Todo",
            'description': "This is a new test todo item.",
            'completed': False
        }

# Create your tests here.
