import datetime
from django.shortcuts import render, redirect
import json
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db.models import Q
import re
from django.conf.urls import url
from core.models import Post, Bookmark, PostLike
# Create your views here.

REGEX_FOR_EMAIL = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
MAX_USERNAME_CHARACTERS = 20
EXCLUDED_USERNAME_CHARACTERS = ['@', '!', '#', '$', '%', '^', '&', '*',
                                '(', ')', '{', '}', '[', ']', '\\', '/', '?', '<', '>', ',', ' ']

# AUTHENTICATION
def check_email(email):
    return re.fullmatch(REGEX_FOR_EMAIL, email)


def check_username(username: str) -> tuple:
    length = 0
    for i in username:
        length += 1
        if length == MAX_USERNAME_CHARACTERS:
            return (False, "Username too long .")
        if i in EXCLUDED_USERNAME_CHARACTERS:
            return (False, 'You Can\'t use ' + i + ' in Username .')
    if length >= 5:
        return (True, None)
    else:
        return (False, 'Minimum 5 characters are required in Username .')


def knowIfLoggedIn(request):
    if request.is_ajax():
        message = False
        if request.user.is_authenticated:
            message = True
        return HttpResponse(json.dumps({'result': str(message)}),
                            content_type="application/json")
    else:
        return HttpResponse("Page Not Found")


def isUserNameAvailable(request):
    if request.method == "POST":
        if request.is_ajax():
            is_available = False
            error = None
            body = request.body.decode('utf-8')
            user_name = json.loads(body)["username"]
            x = list(get_user_model().objects.filter(Q(username=user_name)))
            if len(x) == 0:
                y = check_username(user_name)
                if y[0]:
                    is_available = True
                else:
                    is_available = False
                    error = y[1]
            else:
                error = "Username Occupied"
            response_data = json.dumps(
                {'response': is_available, 'error': error})
            mimetype = 'application/json'
        return HttpResponse(response_data, mimetype)
    else:
        return HttpResponse("Page Not Found")  # TODO


def isEmailAvailable(request):
    if request.method == "POST":
        if request.is_ajax():
            is_available = False
            body = request.body.decode('utf-8')
            email = json.loads(body)["email"]
            x = list(get_user_model().objects.filter(Q(email=email)))
            if (check_email(email) and len(x) == 0):
                is_available = True
            response_data = json.dumps({'response': is_available})
            mimetype = 'application/json'
            return HttpResponse(response_data, mimetype)
    else:
        return HttpResponse("Page Not Found")  # TODO

# NAVBAR/GENERAL
def getRequestUserInfo(request):
    if request.method == "POST":
        if request.is_ajax():
            user = request.user
            data = {'username': user.username, 'name': user.full_name, 'dp_url': user.get_dp_path}
            response_data = json.dumps({'response': data})
            mimetype = 'application/json'
            return HttpResponse(response_data, mimetype)
    else:
        return HttpResponse("Page Not Found")  # TODO

def getSearchResults(request):
    if request.method == "POST":
        if request.is_ajax():
            query = json.loads(request.body.decode('utf-8'))["query"].lower()
            lst = sorted(list(get_user_model().objects.prefetch_related().filter(
            Q(username__icontains=query) | Q(full_name__icontains=query))[0:100]),
                     key=lambda t: [t.get_no_of_followers], reverse=True)
            data = {'response': {}}
            for val in lst:
                try:
                    data['response'][val.username] = {
                        'username': val.username, 'image': val.display_picture.url,
                        'full_name': val.full_name, 'link': f'/{val.username}'}
                except:
                    data['response'][val.username] = {
                        'username': val.username, 'image': '/static/svgs/user.png',
                        'full_name': val.full_name, 'link': f'/{val.username}'}
            response_data = json.dumps({'response': data})
            mimetype = 'application/json'
            return HttpResponse(response_data, mimetype)
    else:
        return HttpResponse("Page Not Found")  # TODO

def getUserSuggestions(request):
    if request.method == 'POST':
        if request.is_ajax():
            suggs =  request.user.get_min_sugg
            response = {}
            for i in suggs:
                response[i.username] = {'username': i.username, 'dp_url': i.get_dp_path, 'name': i.full_name}
            response_data = json.dumps({'response': response})
            mimetype = 'application/json'
            return HttpResponse(response_data, mimetype)
    else:
        return HttpResponse("Page Not Found") # TODO

def knowIfPostWasLiked(request):
    if request.method == 'POST':
        if request.is_ajax():
            t1 = datetime.datetime.now()
            post_id = json.loads(request.body.decode('utf-8'))["custom_id"]
            t2 = datetime.datetime.now()
            print('t1 => ', t2-t1)
            response = Post.objects.prefetch_related().get(custom_id=post_id).was_liked_by_current_user()
            t3 = datetime.datetime.now()
            print('t2 => ', t3-t2)
            response_data = json.dumps({'response': response})
            mimetype = 'application/json'
            t4 = datetime.datetime.now()
            print('t3 => ', t4-t3)
            print(t4-t1)
            return HttpResponse(response_data, mimetype)
    else:
        return HttpResponse("Page Not Found") # TODO

def knowIfPostWasBookmarked(request):
    if request.method == 'POST':
        if request.is_ajax():
            post_id = json.loads(request.body.decode('utf-8'))["custom_id"]
            response = Post.objects.get(custom_id=post_id).was_bookmarked_by_current_user()
            response_data = json.dumps({'response': response})
            mimetype = 'application/json'
            return HttpResponse(response_data, mimetype)
    else:
        return HttpResponse("Page Not Found") # TODO

def addLike(request):
    if request.method == 'POST':
        if request.is_ajax():
            post_id = json.loads(request.body.decode('utf-8'))["custom_id"]
            try:
                post = Post.objects.prefetch_related().get(custom_id=post_id)
                try:
                    PostLike.objects.prefetch_related().get(post=post, user_who_liked_the_post=request.user)
                    response = 'Already Liked'
                except:
                    x = PostLike.objects.create(post=post, user_who_liked_the_post=request.user)
                    x.save()
                    response = 'Liked'
            except:
                response = 'No Post'
            response_data = json.dumps({'response': response})
            mimetype = 'application/json'
            return HttpResponse(response_data, mimetype)
    else:
        return HttpResponse("Page Not Found") # TODO

def removeLike(request):
    if request.method == 'POST':
        if request.is_ajax():
            post_id = json.loads(request.body.decode('utf-8'))["custom_id"]
            try:
                post = Post.objects.prefetch_related().get(custom_id=post_id)
                try:
                    x = PostLike.objects.prefetch_related().get(post=post, user_who_liked_the_post=request.user)
                    x.delete()
                    response = 'Like Removed'
                except:
                    response = 'Already not Liked'
            except:
                response = 'No Post'
            response_data = json.dumps({'response': response})
            mimetype = 'application/json'
            return HttpResponse(response_data, mimetype)
    else:
        return HttpResponse("Page Not Found") # TODO

def addBookmark(request):
    if request.method == 'POST':
        if request.is_ajax():
            post_id = json.loads(request.body.decode('utf-8'))["custom_id"]
            try:
                post = Post.objects.prefetch_related().get(custom_id=post_id)
                try:
                    Bookmark.objects.prefetch_related().get(post=post, user=request.user)
                    response = 'Already Bookmarked'
                except:
                    x = Bookmark.objects.create(post=post, user=request.user)
                    x.save()
                    response = 'Bookmarked'
            except:
                response = 'No Post'
            response_data = json.dumps({'response': response})
            mimetype = 'application/json'
            return HttpResponse(response_data, mimetype)
    else:
        return HttpResponse("Page Not Found") # TODO

def removeBookmark(request):
    if request.method == 'POST':
        if request.is_ajax():
            post_id = json.loads(request.body.decode('utf-8'))["custom_id"]
            try:
                post = Post.objects.prefetch_related().get(custom_id=post_id)
                try:
                    x = Bookmark.objects.prefetch_related().get(post=post, user=request.user)
                    x.delete()
                    response = 'Bookmark Removed'
                except:
                    response = 'Already not Bookmarked'
            except:
                response = 'No Post'
            response_data = json.dumps({'response': response})
            mimetype = 'application/json'
            return HttpResponse(response_data, mimetype)
    else:
        return HttpResponse("Page Not Found") # TODO

def getPostLikes(request):
    if request.method == 'POST':
        if request.is_ajax():
            post_id = json.loads(request.body.decode('utf-8'))["custom_id"]
            try:
                post = Post.objects.prefetch_related().get(custom_id=post_id)
                response = post.get_post_likes_length
            except:
                response = 0
            response_data = json.dumps({'response': response})
            mimetype = 'application/json'
            return HttpResponse(response_data, mimetype)
    else:
        return HttpResponse("Page Not Found") # TODO
