from typing import Counter
from django.shortcuts import render, redirect, HttpResponse
from .models import Post
import json
from django.core import serializers
from django.contrib.auth import get_user_model
import time
from .models import PostList
# Create your views here.

MAX = 1000
posts_per_page = 21 # Actually 20

def checkLogin(user):
    return user.is_authenticated 


def feed(request):
    if request.method == 'GET':
        if checkLogin(request.user):
            return render(request, 'frontend/index.html')
        else:
            return redirect('login/')
    elif request.method == "POST":
        if request.is_ajax():
            page = json.loads(request.body.decode())['page']
            if page == 0:
                pl = PostList()
                pl.save()
            pl = PostList.objects.get(user=request.user)
            posts_dict = dict(json.loads(pl.post_list))
            counter = len(posts_dict.keys())
            start = page*posts_per_page
            stop = (page+1)*posts_per_page
            posts = list(posts_dict.values())
            has_more = True
            if stop <= counter:
                has_more = False
            resp_posts = posts[start : stop]
            
            stop = (resp_posts == [])
            print(stop)
            response = {}
            for i in resp_posts:
                response[i['custom_id']] = i
            resp_posts = json.dumps({'response': response, 'has_more': has_more, 'stop': stop})
            mimetype = 'application/json'
            return HttpResponse(resp_posts, mimetype)
            

    else:
        return HttpResponse("Page Not Found") # TODO
        

def post(request, post_id):
    if checkLogin(request.user):
        return render(request, 'frontend/index.html')
    else:
        return redirect('login/')
    

def profile(request, username):
    if checkLogin(request.user):
        return render(request, 'frontend/index.html')
    else:
        return redirect('login/')