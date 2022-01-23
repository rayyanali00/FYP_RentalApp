from django import forms
from django.db.models import fields
from django.db.models.enums import Choices
from django.forms import ModelForm
from products import models

class CategoryForm(ModelForm):
    class Meta:
        model = models.Product
        fields = ["prod_cat","prod_sub"]
        
class OrderForm(ModelForm):
    country = forms.ChoiceField(label="",
                                initial='',
                                widget=forms.Select(),
                                required=True)
    state = forms.ChoiceField(label="",
                                initial='',
                                widget=forms.Select(),
                                required=True)
    city = forms.ChoiceField(label="",
                                initial='',
                                widget=forms.Select(),
                                required=True)
    class Meta:
        model = models.Order
        fields = ["address","email","total_amount","deliever_at","country","state","city","zip_code",'your_bid_total']
        required = "__all__"
class OrderDelieveryStatusForm(ModelForm):
    class Meta:
        model = models.Order
        fields = ["status"]
        
class ProductForm(ModelForm):
    class Meta:
        model = models.Product
        exclude = ["timePeriod"]
        
class OrderStatusForm(ModelForm):
    class Meta:
        model=models.Order
        fields=['is_accepted']