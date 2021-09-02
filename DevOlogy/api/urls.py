from django.contrib import admin
from django.urls import path, include
from .views import (knowIfLoggedIn, isUserNameAvailable, isEmailAvailable)

urlpatterns = [
    path('isLoggedIn/', knowIfLoggedIn),
    path('isUserNameAvailable/', isUserNameAvailable),
    path('isEmailAvailable/', isEmailAvailable)
]