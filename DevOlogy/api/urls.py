from django.contrib import admin
from django.urls import path, include
from .views import (knowIfLoggedIn, loginUser)

urlpatterns = [
    path('isLoggedIn/', knowIfLoggedIn),
    path('loginUser/', loginUser)
]