from django.contrib import admin
from django.urls import path, include
from .views import index, signin, login, post, profile

urlpatterns = [
    path('', index),
    path('login/', login),
    path('signin/', signin),
    path('post/<str:post_id>', post),
    path('profile/<str:username>/', profile),


]