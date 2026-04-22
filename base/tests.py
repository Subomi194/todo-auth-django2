from base.models import Todo
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
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

    def test_user_registration(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('register')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_create_todo(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('todos')
        response = self.client.post(url, self.todo_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 2)

    def test_get_todo_not_found(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('todo-detail', kwargs={'pk': 1000}) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_todo(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('todos')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Todo.objects.count(), 1)

    def test_get_single_todo(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('todo-detail', kwargs={'pk': self.todo.id}) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_todo(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('todo-detail', kwargs={'pk': self.todo.id}) 
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 0)
        

# Create your tests here.
