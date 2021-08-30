from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return render(request, 'frontend/index.html')
    else:
        return redirect('login/')

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request, 'frontend/index.html')

def signin(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request, 'frontend/index.html')

def post(request, post_id):
    if request.user.is_authenticated:
        return render(request, 'frontend/index.html')
    else:
        return redirect('login/')

def profile(request, username):
    if request.user.is_authenticated:
        return render(request, 'frontend/index.html')
    else:
        return redirect('login/')
