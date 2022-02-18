from django.shortcuts import render , HttpResponse
from FilterTags.templatetags.Filter import getCart , getWishList




def dashboard(request):
    pass


def cart(request):
    context = {}
    context['Cart'] = getCart(request) or []

    return render(request,'cart.html',context)


def wishList(request):
    context = {}
    context['wishList'] = getWishList(request) or []
    return render(request,'wishlist.html',context)