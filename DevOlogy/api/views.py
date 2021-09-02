from django.shortcuts import render, redirect
import json
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db.models import Q
import re
from django.conf.urls import url
# Create your views here.

REGEX_FOR_EMAIL = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
MAX_USERNAME_CHARACTERS = 20
EXCLUDED_USERNAME_CHARACTERS = ['@', '!', '#', '$', '%', '^', '&', '*',
                                '(', ')', '{', '}', '[', ']', '\\', '/', '?', '<', '>', ',', ' ']


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
            response_data = json.dumps({'response': is_available, 'error': error})
            mimetype = 'application/json'
        return HttpResponse(response_data, mimetype)
    else:
        return HttpResponse("Page Not Found")  #TODO


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
        return HttpResponse("Page Not Found")  #TODO
