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

def loginUser(request):
    if request.is_ajax():
        if request.method == "POST":
            login_data = json.loads(request.body)
            username_email = login_data["username"]
            password = login_data["password"]
            try:
                email = get_user_model().objects.get(username=username_email).email
            except:
                email = username_email
                user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                isSuccessful = True
            else:
                isSuccessful = False
            response = {"IsLoginSuccessful" : isSuccessful}
            return HttpResponse(json.dumps(response),
                        content_type="application/json")
    else:
        return HttpResponse("Page Not Found")
