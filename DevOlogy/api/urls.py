from django.contrib import admin
from django.urls import path, include
from .views import (knowIfLoggedIn, isUserNameAvailable, isEmailAvailable, getRequestUserInfo, getSearchResults, getUserSuggestions)

urlpatterns = [
    path('isLoggedIn/', knowIfLoggedIn),
    path('isUserNameAvailable/', isUserNameAvailable),
    path('isEmailAvailable/', isEmailAvailable),
    path('getRequestUserInfo/', getRequestUserInfo),
    path("getSearchResults/", getSearchResults),
    path("getUserSuggestions/", getUserSuggestions),
]