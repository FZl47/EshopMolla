from django.shortcuts import render , HttpResponse
from django.views import View
from django.views.generic import TemplateView , View
from django.contrib.auth.models import User
from Product.models import Product
from django.db.models import F , Min , Max , Avg , Count , Sum , Value
from .models import SiteInfo , OutStor , CommentSupport , FaqCategory
from Config.Tools import ValidationText , ValidationEmail , Set_Cookie_Functionality
import time




class Home(View):
    template_name = 'Home/index.html'

    def get(self,request,*args,**kwargs):
        context = {}
        products = Product.objects.all()
        context['products'] = products
        context['products_recent'] = products.filter(productStock__count__gt=0).distinct()
        return render(request,self.template_name,context)

def aboutUs(request):
    siteInfo = SiteInfo.objects.first()
    return render(request,'AboutUs/index.html',{'SiteInfo':siteInfo})

def contactUs(request):
    context = {}
    siteInfo = SiteInfo.objects.first()
    outStors = OutStor.objects.all()
    context['SiteInfo'] = siteInfo
    context['outStors'] = outStors
    return render(request, 'ContactUs/index.html', context)


def FAQ(request):
    context = {}
    faqCategories = FaqCategory.objects.all()
    context['FaqCategories'] = faqCategories
    return render(request,'FAQ/index.html',context)



def submitCommentContactSupport(request):
    if request.method == 'POST':
        data = request.POST
        name = data.get('name') or None
        email = data.get('email') or None
        phone = data.get('phone') or None
        subject = data.get('subject') or None
        message = data.get('message') or None
        if ValidationText(name,2,101) and ValidationEmail(email,2,101) and ValidationText(phone,10,12) and ValidationText(subject,4,101) and ValidationText(message,2,1001):
            CommentSupport.objects.create(name=name,email=email,phone=phone,subject=subject,message=message)
            return Set_Cookie_Functionality('Your comment submited successfuly','Success')
        return Set_Cookie_Functionality('Please fill in the fields correctly','Error')
    raise PermissionError

# Err

def err_404(request,exception):
    return render(request,'Err/404.html')

def err_500(request):
    return render(request,'Err/500.html')

