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
        products = Product.objects.all()
        return render(request,self.template_name,{'products':products})

