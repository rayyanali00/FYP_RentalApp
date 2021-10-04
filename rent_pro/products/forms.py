from django import forms
from django.db.models import fields
from django.db.models.enums import Choices
from django.forms import ModelForm
from products import models

class CategoryForm(ModelForm):
    class Meta:
        model = models.Product
        fields = ["prod_cat","prod_sub"]