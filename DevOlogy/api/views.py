from django.shortcuts import render
import json
from django.http import HttpResponse
from django.contrib.auth import get_user_model
# Create your views here.

def knowIfLoggedIn(request):
    message = False
    if request.user.is_authenticated:
        message = True
    print(message)
    return HttpResponse(json.dumps({'result': str(message)}),
                       content_type="application/json")
