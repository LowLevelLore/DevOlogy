from django.contrib import admin
from .models import Post, Link, Comment, PostLike, CommentLike, Follow, Bookmark, FollowRequest, PostList

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    fields = ('picture', 'user', 'caption')
    list_display = ('user', 'pk')


class LinkAdmin(admin.ModelAdmin):
    fields = ('user', 'link')
    list_display = ('user', 'pk')


class CommentAdmin(admin.ModelAdmin):
    fields = ('text', 'related_post', 'user_who_commented')
    list_display = ('related_post', 'user_who_commented', 'pk')


class PostLikeAdmin(admin.ModelAdmin):
    fields = ('post', 'user_who_liked_the_post')
    list_display = ('post', 'user_who_liked_the_post')


class CommentLikeAdmin(admin.ModelAdmin):
    fields = ('comment', 'user_who_liked_the_comment')
    list_display = ('comment', 'user_who_liked_the_comment')


class FollowAdmin(admin.ModelAdmin):
    fields = ('user_who_was_followed', 'user_who_followed')
    list_display = ('custom_id', 'followed_on')


class BookmarkAdmin(admin.ModelAdmin):
    fields = ('user', 'post')
    list_display = ('user', 'post')


class FollowRequestAdmin(admin.ModelAdmin):
    fields = ('user_who_requested', 'user_who_was_requested', 'request_was_accepted')
    list_display = ('user_who_requested', 'user_who_was_requested', 'request_was_accepted')


admin.site.register(Post, PostAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(PostLike, PostLikeAdmin)
admin.site.register(CommentLike, CommentLikeAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(FollowRequest, FollowRequestAdmin)
admin.site.register(PostList)
