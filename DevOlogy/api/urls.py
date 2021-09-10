from django.contrib import admin
from django.urls import path, include
from .views import (knowIfLoggedIn, isUserNameAvailable, isEmailAvailable, getRequestUserInfo, getSearchResults,
                    getUserSuggestions, knowIfPostWasLiked, knowIfPostWasBookmarked, addLike, removeLike, addBookmark, removeBookmark, getPostLikes)

urlpatterns = [
    path('isLoggedIn/', knowIfLoggedIn),
    path('isUserNameAvailable/', isUserNameAvailable),
    path('isEmailAvailable/', isEmailAvailable),
    path('getRequestUserInfo/', getRequestUserInfo),
    path("getSearchResults/", getSearchResults),
    path("getUserSuggestions/", getUserSuggestions),
    path("knowIfPostWasLiked/", knowIfPostWasLiked),
    path("knowIfPostWasBookmarked/", knowIfPostWasBookmarked),
    path("addLike/", addLike),
    path("removeLike/", removeLike),
    path("addBookmark/", addBookmark),
    path("removeBookmark/", removeBookmark),
    path("getPostLikes/", getPostLikes)
]
