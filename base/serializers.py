from rest_framework import serializers
from base.models import Todo
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone_number', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(  #calls custom user manager's create_user method
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', '')
        )
        return user
    
class TodoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) #show user details in the todo serializer, but make it read-only to prevent changes to the user through the todo endpoint
    class Meta:
        model = Todo
        fields = ['id', 'user', 'title', 'description', 'completed', 'created_at']
        read_only_fields = ['user', 'created_at']
