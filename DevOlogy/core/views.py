from django.shortcuts import render, redirect, HttpResponse
from .models import Post
import json
from django.core import serializers
from django.contrib.auth import get_user_model
# Create your views here.

MAX = 1000
posts_per_page = 1 # Actually 20

def checkLogin(user):
    return user.is_authenticated 


def feed(request):
    if request.method == "POST":
        following = request.user.get_user_following
        following.append(request.user)
        posts = []
        counter = 0
        for user in following:
            for post in list(Post.objects.prefetch_related().filter(user=user)):
                if counter >= MAX:
                    break
                else:
                    posts.append(post)
                    counter += 1

        posts.sort(key=lambda x: x.posted_on, reverse=True)

    if request.method == 'GET':
        if checkLogin(request.user):
            return render(request, 'frontend/index.html')
        else:
            return redirect('login/')
    elif request.method == "POST":
        if request.is_ajax():
            page = json.loads(request.body.decode())['page']
            start = page*posts_per_page
            stop = (page+1)*posts_per_page
            print(start, stop)
            if stop <= counter:
                has_more = False
            has_more = True
            resp_posts = posts[start : stop]
            
            stop = (resp_posts == [])
            response = {}
            for i in resp_posts:
                response[i.custom_id] = {'custom_id': i.custom_id, 'username': i.user.username, 'picture': i.picture.url, 'caption': i.caption, 'posted_on': str(i.posted_on)}
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