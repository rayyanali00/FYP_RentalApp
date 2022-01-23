from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls.base import reverse_lazy
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from .forms import *
from products.models import Cart, Order
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.serializers import UserGraphSerializer, UserSerializer
from django.db.models.functions import Cast, Trunc
from django.db.models import (Q, 
                            Sum, 
                            F, 
                            Max, 
                            Min,
                            Count,
                            Value,
                            ExpressionWrapper, 
                            DurationField,
                            DecimalField, 
                            DateField,
                            DateTimeField, 
                            TimeField)



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
   
class AdminDashboard(LoginRequiredMixin,TemplateView):
    template_name="admin_dashboard.html"
    
    def get_query_set(self,**args):
        query_set = {
        "total_orders_count":Order.objects.all().count(),
        "delievered_orders":Order.objects.filter(status="Delievered").count(),  
        "accpted_orders":Order.objects.filter(is_accepted="Accept").count()          
        }
        return query_set
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["orders_count"] = self.get_query_set()['total_orders_count']
        context["del_orders"] = self.get_query_set()['delievered_orders']
        context['accepted_order'] = self.get_query_set()['accpted_orders']
        return context
    
class UserListTemplate(LoginRequiredMixin,UserPassesTestMixin,TemplateView):
    template_name="users_list.html"
    
    def test_func(self):
        if self.request.user.user_role=='Admin':
            return True
        else:
            return False
    
@login_required
@api_view(['GET'])
def User_List(request):
    user_obj = User.objects.all()    
    serializer_obj = UserSerializer(user_obj, many=True)
    return Response(serializer_obj.data)
    
@login_required
@api_view(['GET'])
def User_List_Graph(request):
    user_obj = User.objects.all().values(dated=Trunc('date_joined','day')).annotate(counted=Count('id')).values('dated','counted').order_by('dated')    
    serializer_obj = UserGraphSerializer(user_obj, many=True)
    return Response(serializer_obj.data)