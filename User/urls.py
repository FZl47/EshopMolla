from django.urls import path
from . import views

app_name = 'User'
urlpatterns = [
    path('dashboard',views.dashboard,name='dashboard'),
    path('cart',views.cart,name='cart'),
    path('wishList',views.wishList,name='wishList'),
]