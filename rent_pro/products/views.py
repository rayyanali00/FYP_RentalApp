from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from django.views.generic import ListView,FormView,DetailView
from .models import Category, Product, Sub_Category
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CategoryForm
from django.http import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.utils.http import urlencode
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.core import serializers
from django.http import JsonResponse



# Create your views here.
class DashboardClient(LoginRequiredMixin,FormView):
    template_name="dashboard_client.html"
    form_class = CategoryForm
    model = Category

    def get_queryset(self):
        product_list = Product.objects.all()
        page = self.request.GET.get('page',1)
        paginator = Paginator(product_list, 10)
        query_list = {}
        try:
            query_list = {
                "product_list":product_list,
                "product":paginator.page(page)
            }
        except PageNotAnInteger:
            query_list = {
                "product_list":product_list,
                "product":paginator.page(1)
            }
        except EmptyPage:
            query_list = {
                "product_list":product_list,
                "product":paginator.page(paginator.num_pages)
            }
        return query_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"]=self.get_queryset()["product"]
        context["product_list"]=serializers.serialize("json",self.get_queryset()["product_list"])
        print(self.get_queryset())
        return context
    
    # def pos(self, form):
    #     category = form.cleaned_data['prod_cat']
    #     sub_category = form.cleaned_data['prod_sub']
    #     query_params = {
    #         'category':category,
    #         'sub_category':sub_category
    #     }
    #     return HttpResponseRedirect(reverse_lazy('products:products_api')+f'?{urlencode(query_params)}')
    
    
    def post(self, request, *args, **kwargs):
        category = self.request.POST.get('category')
        sub_category = self.request.POST.get('sub_category')
        query_params = {
            'category':category,
            'sub_category':sub_category
        }   
        return HttpResponseRedirect(reverse_lazy('products:products_api')+f'?{urlencode(query_params)}')
    
    # def get_form(self, form_class):
    #     form = super().get_form(form_class=form_class)
    #     form.['prod_cat'].queryset = Rate.objects.filter(company_id=the_company.id)

    
def ProductCategoryApi(request):
        sub_category = Sub_Category.objects.values_list("category__cat_name","sub_category")
        print(sub_category)
        dct = dict((y,x) for x,y in sub_category)
        lst_dct = {}
        lst_dct['Furniture'] = [k for k, v in dct.items() if v == 'Furniture']
        lst_dct['ElectricAppliances'] = [k for k, v in dct.items() if v == 'ElectricAppliances']
        lst_dct['FitnessEquipment'] = [k for k, v in dct.items() if v == 'FitnessEquipment']
        lst_dct['Crockery'] = [k for k, v in dct.items() if v == 'Crockery']
        return JsonResponse(lst_dct, safe=False)
          
class ProductListFilter(LoginRequiredMixin,ListView):
    template_name="dashboard_client.html"
    def get_queryset(self):

        if self.request.method=="GET":
            query_set = {}
            cat = self.request.GET.get('category',None)
            sub_cat = self.request.GET.get('sub_category',None)
            
            if cat is not None and sub_cat is not None:
                query_set = Product.objects.filter(prod_cat__cat_name__contains=cat,prod_sub__sub_category__contains=sub_cat)
                return query_set
        return query_set
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["products"] = self.get_queryset()
        return context
    
class ProductDetailView(LoginRequiredMixin,DetailView):
    template_name="product_detail.html"
    model = Product