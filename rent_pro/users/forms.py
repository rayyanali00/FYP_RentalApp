from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ["username","email","password1","password2"]
        