from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from django.views.generic import ListView,FormView,DetailView
from .models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CategoryForm
from django.http import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.utils.http import urlencode
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
class DashboardClient(LoginRequiredMixin,FormView):
    template_name="dashboard_client.html"
    form_class = CategoryForm

    def get_queryset(self):
        product_list = Product.objects.all()        
        page = self.request.GET.get('page',1)
        paginator = Paginator(product_list, 10)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        return products
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"]=self.get_queryset()
        print(self.get_queryset())
        return context
    
    def form_valid(self, form):
        category = form.cleaned_data['prod_cat']
        sub_category = form.cleaned_data['prod_sub']
        query_params = {
            'category':category,
            'sub_category':sub_category
        }
        return HttpResponseRedirect(reverse_lazy('products:products_api')+f'?{urlencode(query_params)}')
    
    
    
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