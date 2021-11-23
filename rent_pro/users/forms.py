from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","email","password1","password2",]
        
        
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields=["first_name","last_name","email"]
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"