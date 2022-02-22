from django.urls import path
from . import views

app_name = 'Public'
urlpatterns = [
    path('',views.Home.as_view(),name='home'),
    path('aboutUs',views.aboutUs,name='aboutUs'),
    path('contactUs',views.contactUs,name='contactUs'),
    path('FAQ',views.FAQ,name='FAQ'),
    path('submitCommentContactSupport',views.submitCommentContactSupport,name='submitCommentContactSupport'),
]

