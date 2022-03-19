from django.urls import path
from . import views


app_name = 'Product'
urlpatterns = [
    path('products',views.products.as_view(),name='products'),
    path('category/<str:title>',views.category.as_view(),name='category'),
    path('product/<slug>',views.product.as_view(),name='product'),
    path('product/<slug>/getStockProduct/<int:id>/<str:type>',views.getStockProduct,name='getStockProduct'),
    path('product/<slug>/addProductToCart',views.addProductToCart,name='addProductToCart'),
    path('product/<slug>/addProductToWishList',views.addProductToWishList,name='addProductToWishList'),
    path('removeDetailCart',views.removeDetailCart,name='removeDetailCart'),
    path('removeDetailWish',views.removeDetailWish,name='removeDetailWish'),
    path('product/<slug>/addComment', views.addComment, name='addComment'),
    path('checkCoupon', views.checkCoupon, name='checkCoupon'),
]