from django.shortcuts import render , HttpResponse
from django.views import View
from django.views.generic import TemplateView , View
from django.contrib.auth.models import User
from Product.models import Product
from django.db.models import F , Min , Max , Avg , Count , Sum , Value
import time




class Home(View):
    template_name = 'Home/index.html'

    def get(self,request,*args,**kwargs):
        context = {}
        products = Product.objects.all()
        context['products'] = products
        context['products_recent'] = products.filter(productStock__count__gt=0).distinct()
        return render(request,self.template_name,context)

