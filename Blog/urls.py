from django.urls import path
from . import views


app_name = 'Blog'
urlpatterns = [
    path('blogs',views.blogs,name='blogs')
]