from django.urls import path
from . import views


app_name = 'Blog'
urlpatterns = [
    path('posts',views.posts,name='posts'),
    path('category/<str:slug>',views.category,name='category'),
    path('tag/<str:slug>',views.tag,name='tag'),
    path('post/<str:slug>',views.post,name='post'),
    path('saved',views.saved,name='saved'),
    path('post/save/<int:id>',views.save_post,name='save_post'),
    path('post/like/<int:id>',views.like_post,name='like_post'),
    path('post/comment/',views.comment_post,name='comment_post'),
]