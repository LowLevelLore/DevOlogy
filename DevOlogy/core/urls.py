from django.contrib import admin
from django.urls import path, include
from .views import index, post, profile

urlpatterns = [
    path('', index),
    path('post/<str:post_id>', post),
    path('profile/<str:username>/', profile),
]