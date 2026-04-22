from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)

# BaseUserManager is used to create a custom user manager for the User model. It provides methods for creating users and superusers.

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields): # The create_user method is responsible for creating a regular user. It takes an email, password, and any additional fields as arguments. It checks if the email is provided, normalizes it, creates a user instance, sets the password, and saves the user to the database.
        if not email:
            raise ValueError("Email is required")
        
        email = self.normalize_email(email) # Normalize the email address by lowercasing the domain part
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields): # The create_superuser method is responsible for creating a superuser. It takes an email, password, and any additional fields as arguments. It sets the is_staff and is_superuser fields to True, checks if they are set correctly, and then calls the create_user method to create the superuser.
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin): # The User model is a custom user model that inherits from AbstractBaseUser and PermissionsMixin. It defines the fields for the user, such as email, first_name, last_name, phone_number, is_active, is_staff, created_at, and is_superuser. It also specifies the custom user manager to be used for creating users and superusers. The USERNAME_FIELD is set to 'email', which means that the email field will be used as the unique identifier for authentication instead of the default username field.
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
class Todo(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')
    title = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

