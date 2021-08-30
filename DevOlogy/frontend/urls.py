from django.contrib import admin
from django.urls import path, include
from .views import index

urlpatterns = [
    path('', index),
    path('login/', index),
    path('signin/', index),
    path('post/<str:post_id>', index),
    path('profile/<str:username>/', index),


]