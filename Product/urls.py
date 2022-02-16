from django.urls import path
from . import views


app_name = 'Product'
urlpatterns = [
    path('products',views.products.as_view(),name='products'),
    path('product/<slug:slug>',views.product.as_view(),name='product'),
    path('product/<slug:slug>/getStockProduct/<int:id>/<str:type>',views.getStockProduct,name='getStockProduct'),
    path('product/<slug:slug>/addProductToCart',views.addProductToCart,name='addProductToCart'),
    path('product/<slug:slug>/addProductToWishList',views.addProductToWishList,name='addProductToWishList'),
    path('removeDetailCart',views.removeDetailCart,name='removeDetailCart'),
]