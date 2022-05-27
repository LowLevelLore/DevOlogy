from typing import Counter
from django.shortcuts import render, redirect, HttpResponse
from .models import Post
import json
from django.core import serializers
from django.contrib.auth import get_user_model
import time
from .models import PostList, CommentList
# Create your views here.

MAX = 1000
POSTS_PER_PAGE = 21
COMMENTS_PER_PAGE = 11


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
            start = page*POSTS_PER_PAGE
            stop = (page+1)*POSTS_PER_PAGE
            posts = list(posts_dict.values())
            has_more = True
            if stop >= counter:
                has_more = False
            resp_posts = posts[start: stop]

            stop = (resp_posts == [])
            response = {}
            for i in resp_posts:
                response[i['custom_id']] = i
            resp_posts = json.dumps(
                {'response': response, 'has_more': has_more, 'stop': stop})
            mimetype = 'application/json'
            return HttpResponse(resp_posts, mimetype)

    else:
        return HttpResponse("Page Not Found")  # TODO


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


def getComments(request):
    if request.method == 'POST':
        if request.is_ajax():
            post_id = json.loads(request.body.decode())['post_id']
            try:
                post = Post.objects.get(custom_id=post_id)
                page = json.loads(request.body.decode())['page']
                if page == 0:
                    comment_list = CommentList(post=post)
                    comment_list.save()

                cl = CommentList.objects.get(post=post)

                comments_dict = dict(json.loads(cl.comments_list))
                counter = len(comments_dict.keys())
                start = page*COMMENTS_PER_PAGE
                stop = (page+1)*COMMENTS_PER_PAGE
                comments = list(comments_dict.values())
                has_more = True
                if stop >= counter:
                    has_more = False
                resp_comments = comments[start: stop]
                stop = (resp_comments == [])
                data = {}
                for i in resp_comments:
                    data[i['custom_id']] = i
                resp_comments = json.dumps({'data': data, 'response': "Successful",
                                           'has_more': has_more, 'stop': stop, 'status': 200, 'total': counter})
                mimetype = 'application/json'
                return HttpResponse(resp_comments, mimetype)

            except:
                resp_comments = json.dumps(
                    {'response': 'Unsuccessful', 'status': 404})
                mimetype = 'application/json'
                return HttpResponse(resp_comments, mimetype)
