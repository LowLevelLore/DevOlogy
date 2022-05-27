from django.contrib import admin
from django.urls import path, include
from .views import (deleteComment, knowIfLoggedIn, isUserNameAvailable, isEmailAvailable,
                    getRequestUserInfo, getSearchResults, getUserSuggestions,
                    knowPostLikesAndBookmarks,  addLike, removeLike, addBookmark,
                    removeBookmark, getPostData, comment, addCommentLike,
                    removeCommentLike, deleteComment, getIdFromUserName, getBioData,
                    getFollowerFollowing, getProfileUserData, getProfilePosts)
from core.views import getComments

urlpatterns = [
    path('user/isLoggedIn/', knowIfLoggedIn),
    path('auth/isUserNameAvailable/', isUserNameAvailable),
    path('auth/isEmailAvailable/', isEmailAvailable),
    path('user/getRequestUserInfo/', getRequestUserInfo),
    path("general/getSearchResults/", getSearchResults),
    path("user/getUserSuggestions/", getUserSuggestions),
    path("post/knowPostLikesAndBookmarks/", knowPostLikesAndBookmarks),
    path("post/addLike/", addLike),
    path("post/removeLike/", removeLike),
    path("post/addBookmark/", addBookmark),
    path("post/removeBookmark/", removeBookmark),
    path("post/getPostData/", getPostData),
    path("post/comment/", comment),
    path("post/getComments/", getComments),
    path("post/addCommentLike/", addCommentLike),
    path("post/removeCommentLike/", removeCommentLike),
    path("post/deleteComment/", deleteComment),
    path("user/getIdFromUserName/", getIdFromUserName),
    path("user/getBioData/", getBioData),
    path("user/getFollowerFollowing/", getFollowerFollowing),
    path("user/getProfileUserData/", getProfileUserData),
    path("user/getProfilePosts/", getProfilePosts),
]
