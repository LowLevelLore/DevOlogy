from django.shortcuts import render, redirect
import json
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
# Create your views here.

def knowIfLoggedIn(request):
    if request.is_ajax():
        message = False
        if request.user.is_authenticated:
            message = True
        return HttpResponse(json.dumps({'result': str(message)}),
                        content_type="application/json")
    else:
        return HttpResponse("Page Not Found")

