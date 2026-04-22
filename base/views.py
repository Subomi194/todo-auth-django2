from django.shortcuts import render
from base.serializers import UserSerializer, TodoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

from base.models import Todo
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes


# Create your views here.

class UserRegistrationView (APIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny,]

    @extend_schema(
            request=UserSerializer
    ) # for Swagger docs

    def post(self, request) :
        user = request.user
        print("WHO IS REGISTERING",user)
        serializer = UserSerializer (data=request.data)
        if serializer.is_valid():
            serializer.save() # Set the user field to the current user when saving the todo
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class TodoListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TodoSerializer

    @extend_schema(
            request=TodoSerializer
    )

    def get (self, request) :
        # Filter todos to only return the current user's todos
        todo = Todo.objects.filter(user=request.user)
        serializer = TodoSerializer(todo, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def post (self, request) :
        data = request.data
        user = request.user
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user) # Set the user field to the current user when saving the todo
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated,]

    def get(self, request, pk):
        try:
            #user=request.user ensure the user can only access their own todos
            todo = Todo.objects.get(pk=pk, user=request.user) # Ensure the user can only access their own todos
        except Todo.DoesNotExist:
            return Response(data={'error': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk, user=request.user) # Ensure the user can only delete their own todos
        except Todo.DoesNotExist:
            return Response(data={'error': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)
        todo.delete()
        return Response(data={'message': 'Todo deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class TodoPaginatedView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    permission_classes = [permissions.AllowAny,]

    def list (self, request):
        queryset = self.get_queryset()
        serializer = TodoSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ListAllTodos(APIView):
    serializer_class = TodoSerializer
    pagination_class = PageNumberPagination

    def get(self, request):
        q = self.request.query_params.get('q', None)

        print("QUERY PARAMS", q)

        if q is not None:
            todos = Todo.objects.filter(title__icontains=q) # Filter todos based on the query parameter 'q' in the title field
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(todos, request)
            serializer = TodoSerializer(page, many=True) #expecting multiple records so turn it into a list of multiple dictionaries
        else:
            todos = Todo.objects.all()
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(todos, request)
            serializer = TodoSerializer(page, many=True) #expecting multiple records so turn it into a list of multiple dictionaries
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class ListAllTodosWithLimitOffsetPagination(APIView):
    pagination_class = LimitOffsetPagination

    def get(self, request):
        todos = Todo.objects.all()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(todos, request)
        serializer = TodoSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data) 

# class ListAllTodosWithCursorPagination(APIView):
#     pagination_class = CursorPagination
#     ordering = 'created_at'  # Ensure the model has a created_at field for cursor pagination to work

#     def get(self, request):
#         todos = Todo.objects.all()
#         paginator = self.pagination_class()
#         page = paginator.paginate_queryset(todos, request)
#         serializer = TodoSerializer(page, many=True)
#         return paginator.get_paginated_response(serializer.data)
    

class TodoCursorPagination(CursorPagination):
    page_size = 10
    ordering = '-created_at' 

class ListAllTodosWithCursorPagination(APIView):
    pagination_class = TodoCursorPagination  # ← use your custom class

    def get(self, request):
        todos = Todo.objects.all()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(todos, request)
        serializer = TodoSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    

        