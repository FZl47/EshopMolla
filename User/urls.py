from django.urls import path
from . import views

app_name = 'User'
urlpatterns = [
    path('dashboard',views.dashboard,name='dashboard'),
    path('wishList',views.wishList,name='wishList'),
    path('cart',views.cart,name='cart'),
    path('proccedToCheckout',views.proccedToCheckout,name='proccedToCheckout'),
    path('checkout',views.checkout,name='checkout'),
    path('proccedToPayment',views.proccedToPayment,name='proccedToPayment'),
    path('login-register',views.login_register,name='login_register'),
    path('login-register/register',views.register,name='register'),
    path('login-register/login',views.login,name='login'),
    path('logout',views.logout_view,name='logout'),
    path('submitInfo',views.submitInfo,name='submitInfo'),
    path('addAddress',views.addAddress,name='addAddress'),
    path('changeAddress',views.changeAddress,name='changeAddress'),
    path('order/get/<int:id>',views.getOrder,name='getOrder'),
]