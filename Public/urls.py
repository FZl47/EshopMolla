from django.urls import path
from . import views

app_name = 'Public'
urlpatterns = [
    path('',views.Home.as_view(),name='home'),
    path('aboutUs',views.Home.as_view(),name='aboutUs'),
    path('contactUs',views.Home.as_view(),name='contactUs'),
]