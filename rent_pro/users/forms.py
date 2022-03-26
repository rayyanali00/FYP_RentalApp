from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']


class UserUpdateForm(forms.ModelForm):
    """
    This form is used on the profile update page. When the user 
    expects to update certain information from the profile page that 
    belongs to the User table, then we will use this form to display 
    those fields on the profile update page and the respective data
    will be automatically updated in the user table
    """
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['first_name','last_name', 'email']
        # fields = ['email',]
        # exclude = ('first_name','last_name',)


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