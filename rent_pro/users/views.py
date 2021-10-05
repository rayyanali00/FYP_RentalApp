from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls.base import reverse_lazy
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from .forms import *


User = get_user_model()
# Create your views here.
class Index(TemplateView):
    template_name="test.html"

class RegisterUser(SuccessMessageMixin,CreateView):
    model = User
    template_name = "register.html"
    form_class = CreateUser
    success_message = 'Your account has created'
    def get_success_url(self):
        g = Group.objects.get(name='customers') # assuming you have a group 'test' created already. check the auth_user_group table in your DB
        g.user_set.add(self.object)
        return reverse_lazy('users:login')
        
class UpdateProfile(LoginRequiredMixin, View):
    pass
    
class Test(LoginRequiredMixin,TemplateView):
    template_name="test.html"
    redirect_field_name = None
   