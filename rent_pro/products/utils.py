from django.http import request,HttpResponse
import json

def get_cart_data(request):
    if request.method == 'POST':
        data_dict = request.POST.get('')