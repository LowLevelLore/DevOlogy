from django.contrib import admin
from django.urls import path, include
from .views import feed, post, profile

urlpatterns = [
    path('', feed),
    path('post/<str:post_id>/', post),
    path('profile/<str:username>/', profile),
]