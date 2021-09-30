from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class DashboardClient(TemplateView):
    template_name="dashboard_client.html"