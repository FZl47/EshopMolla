from django.shortcuts import render
from django.views.generic import View
from User.models import User
from Product.models import Product

class products(View):
    template_name = 'Products/index.html'

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)
