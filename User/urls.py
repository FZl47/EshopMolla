from django.urls import path
from . import views

app_name = 'User'
urlpatterns = [
    path('cart',views.cart,name='cart'),
]