from django.urls import path
from . import views


app_name = 'Product'
urlpatterns = [
    path('products',views.products.as_view(),name='products'),
    path('product/<slug:slug>',views.product.as_view(),name='product')
]