from django.shortcuts import render , HttpResponse

def cart(request):
    return HttpResponse('cart')


def wishList(request):
    return HttpResponse('wishList')