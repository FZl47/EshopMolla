from django.shortcuts import render
from django.http import JsonResponse
from django.http import Http404
from django.core.exceptions import PermissionDenied
from Config.settings import BASE_URL_BLOG_API, KEY_API
from Config.Tools import Set_Cookie_Functionality
import requests


def getKeyUser(request):
    user = request.user
    if user.id != None:
        return user.keyBlog
    return None


def ConfigAPI(request):
    return {
        'keyUser': getKeyUser(request),
        'keyAPI': KEY_API,
        'BASE_URL_BLOG_API': BASE_URL_BLOG_API,
        'URL': request.build_absolute_uri(),
        'DOMAIN':f"{request.scheme}://{request.get_host()}",
        'PAGE':request.GET.get('page') or 1
    }


def posts(request):
    searchValue = request.GET.get('search')
    isSearched = (searchValue != None and searchValue != '')
    if isSearched:
        URL_GET_POSTS_API = f"{BASE_URL_BLOG_API}/Api/get-posts/search"
        data = ConfigAPI(request)
        data['search'] = searchValue
        response = requests.request('POST', URL_GET_POSTS_API, data=data)
    else:
        URL_GET_POSTS_API = f"{BASE_URL_BLOG_API}/Api/get-posts"
        data = ConfigAPI(request)
        response = requests.request('POST', URL_GET_POSTS_API, data=data)

    if response.status_code == 200:
        response = response.json()
        response['searchValue'] = searchValue
        response['isSearched'] = isSearched
        response['detailPageTitle'] = 'Posts'
        response['detailPageDes'] = 'Blog'
        response['Place'] = 'posts_view'
        response['BASE_URL_BLOG_API'] = BASE_URL_BLOG_API
        return render(request, 'posts.html', response)
    raise Http404


def category(request, slug):
    context = {}
    URL_GET_POSTS_API = f"{BASE_URL_BLOG_API}/Api/get-posts-by-category/{slug}"
    data = ConfigAPI(request)
    response = requests.request('POST', URL_GET_POSTS_API, data=data)
    if response.status_code == 200:
        response = response.json()
        response['detailPageTitle'] = 'Category'
        response['detailPageDes'] = response['Category']['title']
        response['Place'] = 'category_view'
        response['BASE_URL_BLOG_API'] = BASE_URL_BLOG_API
        return render(request, 'posts.html', response)
    raise Http404


def tag(request, slug):
    context = {}
    URL_GET_POSTS_API = f"{BASE_URL_BLOG_API}/Api/get-posts-by-tag/{slug}"
    data = ConfigAPI(request)
    response = requests.request('POST', URL_GET_POSTS_API, data=data)
    if response.status_code == 200:
        response = response.json()
        response['detailPageTitle'] = 'Tag'
        response['detailPageDes'] = response['Tag']['title']
        response['Place'] = 'tag_view'
        response['BASE_URL_BLOG_API'] = BASE_URL_BLOG_API
        return render(request, 'posts.html', response)
    raise Http404


def post(request, slug):
    URL_GET_POST_API = f"{BASE_URL_BLOG_API}/Api/get-post"
    data = ConfigAPI(request)
    data['slug'] = slug
    response = requests.request('POST', URL_GET_POST_API, data=data)
    if response.status_code == 200:
        response = response.json()
        response['urlPost'] = request.build_absolute_uri()
        response['BASE_URL_BLOG_API'] = BASE_URL_BLOG_API
        return render(request, 'post.html', response)
    raise Http404


def saved(request):
    URL_GET_POST_SAVED_API = f"{BASE_URL_BLOG_API}/Api/get-saved-posts/"
    data = ConfigAPI(request)
    response = requests.request('POST',URL_GET_POST_SAVED_API,data=data)
    if response.status_code == 200:
        response = response.json()
        response['detailPageTitle'] = 'Posts'
        response['detailPageDes'] = 'Saved'
        response['Place'] = 'saved_view'
        response['BASE_URL_BLOG_API'] = BASE_URL_BLOG_API
        return render(request, 'posts.html',response)
    raise Http404

def save_post(request, id):
    context = {}
    if request.method == 'POST' and request.is_ajax():
        if request.user.id != None:
            URL_ACTION_SAVE_POST = f"{BASE_URL_BLOG_API}/Api/post/save"
            data = {
                'id': id,
                'keyUser': request.user.keyBlog
            }
            response = requests.request('POST', URL_ACTION_SAVE_POST, data=data)
            if response.status_code == 200:
                response = response.json()
                context = response
        else:
            context['status_code'] = 404
            context['status_text'] = 'User not found'
    else:
        context['status_code'] = 403
        context['status_text'] = 'Method not allowed'

    return JsonResponse(context)


def like_post(request,id):
    context = {}
    if request.method == 'POST' and request.is_ajax():
        if request.user.id != None:
            URL_ACTION_LIKE_POST = f"{BASE_URL_BLOG_API}/Api/post/like"
            data = {
                'id': id,
                'keyUser': request.user.keyBlog
            }
            response = requests.request('POST', URL_ACTION_LIKE_POST, data=data)
            if response.status_code == 200:
                response = response.json()
                context = response
        else:
            context['status_code'] = 404
            context['status_text'] = 'User not found'
    else:
        context['status_code'] = 403
        context['status_text'] = 'Method not allowed'

    return JsonResponse(context)


def comment_post(request):
    if request.method == 'POST' and request.user.id != None:
        URL_COMMENT_POST = f"{BASE_URL_BLOG_API}/Api/post/comment"
        data = request.POST.copy()
        data.update({
            'keyUser':request.user.keyBlog
        })
        response = requests.request('POST',URL_COMMENT_POST,data=data)
        if response.status_code == 200:
            response = response.json()
            status = response['status_code']
            if status == 200:
                return Set_Cookie_Functionality('Your comment submited successfully','Success')
            return Set_Cookie_Functionality(response['status_text'],'Error')
        return Set_Cookie_Functionality('Something went wrong','Error')
    raise PermissionDenied