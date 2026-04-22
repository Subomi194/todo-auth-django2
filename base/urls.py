from base.views import UserRegistrationView, TodoListCreateView, TodoDetailView, TodoPaginatedView, ListAllTodos, ListAllTodosWithLimitOffsetPagination, ListAllTodosWithCursorPagination
from django.urls import path

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('todos/', TodoListCreateView.as_view(), name='todos'),
    path('todos/<int:pk>/', TodoDetailView.as_view(), name='todo-detail'),
    path('paginated-todo/', TodoPaginatedView.as_view(), name='paginated-todos'),
    path('all-todos/', ListAllTodos.as_view(), name='all-todos/'),
    path('todos-with-limit-offset/', ListAllTodosWithLimitOffsetPagination.as_view(), name='todo-limit-offset'),
    path('todos-with-cursor-pagination/', ListAllTodosWithCursorPagination.as_view(), name='todo-cursor-pagination'),
]