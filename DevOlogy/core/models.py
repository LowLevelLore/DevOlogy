import datetime
import json

from django.db import models
from django.contrib.auth import get_user_model
from crum import get_current_user
from django.utils.timezone import utc
import django.core.exceptions as ex
import string
import random

# Create your models here.


max_links = 3
id_length = 20
MAX = 2000


def get_post_upload_path(instance, filename):
    return instance.get_upload_path(filename)

def get_post_list():
    following = get_current_user().get_user_following
    following.append(get_current_user())
    posts = []
    counter = 0
    for user in following:
        print(user)
        for post in list(Post.objects.prefetch_related().filter(user=user)):
                if counter >= MAX:
                    break
                else:
                    posts.append(post)
                    counter += 1

    posts.sort(key=lambda x: x.posted_on, reverse=True)
    response = {}
    for i in posts:
                response[i.custom_id] = {'user_dp': i.user.get_dp_path, 'custom_id': i.custom_id, 'username': i.user.username, 'picture': i.picture.url, 'caption': i.caption, 'posted_on': str(i.posted_on)}
    print(json.dumps(response))
    return json.dumps(response)


def make_custom_string_as_id(instance):
    if instance == 'Post':
        instance = Post
    elif instance == 'Link':
        instance = Link
    elif instance == 'Comment':
        instance = Comment
    elif instance == 'PostLike':
        instance = PostLike
    elif instance == 'CommentLike':
        instance = CommentLike
    elif instance == 'Follow':
        instance = Follow
    elif instance == 'Bookmark':
        instance = Bookmark
    elif instance == 'FollowRequest':
        instance = FollowRequest
    elif instance == "PostList":
        instance = PostList
    else:
        return None

    satisfied = False
    while not satisfied:
        custom_string = ''.join(random.choice(string.ascii_uppercase) for _ in range(id_length))
        check_list = list(instance.objects.filter(custom_id=custom_string))
        if len(check_list) == 0:
            satisfied = True

    return custom_string


class Post(models.Model):
    custom_id = models.CharField(max_length=id_length, unique=True, null=False, editable=False, blank=False)
    picture = models.ImageField(upload_to=get_post_upload_path, null=False, blank=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='users_posts')
    caption = models.CharField(max_length=1000, null=True, blank=True, default='')
    posted_on = models.DateTimeField(auto_now_add=True)
    edited_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.custom_id == '' or self.custom_id is None:
            self.custom_id = make_custom_string_as_id('Post')
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return str(f'{str(self.user)} --> {self.pk}')

    def get_upload_path(self, filename):
        return f'UserSpecific/{str(self.user)}/Posts/{str(datetime.datetime.now())}.jpg'

    @property
    def get_post_comments(self) -> list:
        """
        :return: all the comments related to the particular post
        """
        return list(self.posts_comments.prefetch_related().all())

    @property
    def get_post_comments_length(self) -> int:
        """
        :return: the number of comments associated with that particular post
        """
        return len(list(self.posts_comments.prefetch_related().all()))

    @property
    def get_post_likes(self) -> list:
        """
        :return: all the likes related to the particular post
        I know it will not be useful , but.....
        """
        return list(self.post_likes.prefetch_related().all())

    @property
    def get_post_likes_length(self) -> int:
        """
        :return: the number of likes associated with that particular post
        """
        return len(list(self.post_likes.prefetch_related().all()))

    def get_time_diff(self):
        """
        :return: the time ago which post was posted ...
        """
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        diff = now - self.posted_on
        td = float(diff.total_seconds())
        if 60 <= td < 3600:
            response = f'{int(round(td / 60, 0))} MINUTES AGO'
        elif 3600 <= td < 86400:
            response = f'{int(round((td / 3600), 0))} HOURS AGO'
        elif 86400 <= td < 2592000:
            response = f'{int(round((td / 86400), 0))} DAYS AGO'
        elif 2592000 <= td < 31104000:
            response = f'{int(round((td / 2592000), 0))} MONTHS AGO'
        elif 31104000 <= td < 155520000:
            response = f'{int(round((td / 31104000), 0))} YEARS AGO'
        elif td >= 155520000:
            response = f'LONG TIME AGO ..'
        else:
            response = f'JUST NOW'
        return response

    def delete(self, *args, **kwargs):

        this = Post.objects.get(pk=self.pk)
        this.picture.delete(save=False)
        super(Post, self).delete(*args, **kwargs)

    def was_liked_by_current_user(self):
        try:
            PostLike.objects.select_related('post').prefetch_related().get(post=self, user_who_liked_the_post=get_current_user())

            return True
        except ex.ObjectDoesNotExist:
            return False

    def was_bookmarked_by_current_user(self):
        try:
            Bookmark.objects.select_related('post').prefetch_related().get(post=self, user=get_current_user())
            return True
        except:
            return False

    


class Link(models.Model):
    custom_id = models.CharField(max_length=id_length, unique=True, null=False, editable=False, blank=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='bioLinks')
    link = models.URLField(max_length=600)

    def __str__(self):
        return str(f'{str(self.user)} --> {self.link}')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.custom_id == '' or self.custom_id is None:
            self.custom_id = make_custom_string_as_id('Link')
        if self.user.get_bio_links_length >= max_links:
            pass  # Raise ValueError that maximum limit has been reached
        else:
            super(Link, self).save(force_update=force_update, force_insert=force_insert,
                                   using=using, update_fields=update_fields)


class Comment(models.Model):
    custom_id = models.CharField(max_length=id_length, unique=True, null=False, editable=False, blank=False)
    text = models.CharField(max_length=300, null=False, blank=False)
    user_who_commented = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    related_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='posts_comments')
    commented_on = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.custom_id == '' or self.custom_id is None:
            self.custom_id = make_custom_string_as_id('Comment')
        super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return str(f'{self.related_post.pk} --> {self.text}')

    def get_time_diff(self):
        """
        :return: the time ago which post was posted ...
        """
        diff = datetime.datetime.now() - self.commented_on
        print(diff)

    @property
    def get_comment_likes(self) -> list:
        """
        :return: all the likes related to the particular comment
        I know it will not be useful , but.....
        """
        return list(self.comment_likes.all())

    @property
    def get_comment_likes_length(self) -> int:
        """
        :return: the number of likes associated with that particular comment
        """
        return len(list(self.comment_likes.all()))

    @property
    def was_liked_by_current_user(self):
        try:
            CommentLike.objects.get(comment=self, user_who_liked_the_comment=get_current_user())
            return True
        except:
            return False


class PostLike(models.Model):
    custom_id = models.CharField(max_length=id_length, null=False, unique=True, editable=False, blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    user_who_liked_the_post = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                                related_name='user_who_liked_the_post')
    post_liked_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f'{str(self.user_who_liked_the_post)} --> {str(self.post)}')

    def save(self,*args, **kwargs):
        if self.custom_id == '' or self.custom_id is None:
            self.custom_id = make_custom_string_as_id('PostLike')
        try:
            PostLike.objects.prefetch_related().get(user_who_liked_the_post= self.user_who_liked_the_post)
        
        except:
            super(PostLike, self).save(*args, **kwargs)


class CommentLike(models.Model):
    custom_id = models.CharField(max_length=id_length, null=False, editable=False, unique=True, blank=False)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_likes')
    user_who_liked_the_comment = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                                   related_name='user_who_liked_the_comment')
    comment_liked_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f'{str(self.user_who_liked_the_comment)} --> {str(self.comment)}')

    def save(self, *args, **kwargs):
        if self.custom_id == '' or self.custom_id is None:
            self.custom_id = make_custom_string_as_id('CommentLike')
        try:
            CommentLike.objects.prefetch_related().get(user_who_liked_the_comment= self.user_who_liked_the_comment)
        
        except:
            super(CommentLike, self).save(*args, **kwargs)


class Follow(models.Model):
    custom_id = models.CharField(max_length=id_length, null=False, editable=False, blank=False, unique=True)
    user_who_was_followed = models.ForeignKey(get_user_model(),
                                              on_delete=models.CASCADE, related_name='user_who_was_followed')
    user_who_followed = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                          related_name='user_who_followed')
    followed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f'{str(self.user_who_followed)} --> {str(self.user_who_was_followed)}')

    def save(self, *args, **kwargs):
        if self.custom_id == '' or self.custom_id is None:
            self.custom_id = make_custom_string_as_id('Follow')
        try:
            Follow.objects.prefetch_related().get(user_who_followed=self.user_who_followed, user_who_was_followed=self.user_who_was_followed)
        
        except:
            super(Follow, self).save(*args, **kwargs)


class Bookmark(models.Model):
    custom_id = models.CharField(max_length=id_length, null=False, editable=False, blank=False, unique=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.custom_id == '' or self.custom_id is None:
            self.custom_id = make_custom_string_as_id('Bookmark')
        check_list = list(Bookmark.objects.prefetch_related().filter(post=self.post, user=self.user))
        if len(check_list) == 0:
            super(Bookmark, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} -bookmarked- {self.post.pk}'


class FollowRequest(models.Model):
    custom_id = models.CharField(max_length=id_length, null=False, editable=False, blank=False, unique=True)
    user_who_requested = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                           related_name='user_who_will_follow')
    user_who_was_requested = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                               related_name='user_who_will_be_followed')
    request_sent_on = models.DateTimeField(auto_now_add=True)
    request_was_accepted = models.BooleanField()

    def save(self, *args, **kwargs):
        qs = FollowRequest.objects.prefetch_related().filter(user_who_requested=self.user_who_requested,
                                          user_who_was_requested=self.user_who_was_requested)
        if len(qs) == 0:
            if self.custom_id == '' or self.custom_id is None:
                self.custom_id = make_custom_string_as_id('FollowRequest')
            super(FollowRequest, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.request_was_accepted:
            follow = Follow.objexts.create(user_who_was_followed=self.user_who_was_requested,
                                           user_who_followed=self.user_who_requested)
            follow.save()
        super(FollowRequest, self).delete(*args, **kwargs)

class PostList(models.Model):
    custom_id = models.CharField(max_length=id_length, null=False, editable=False, blank=False, unique=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user')
    updated_on = models.DateTimeField(auto_now_add=True)
    post_list = models.JSONField()

    def save(self, *args, **kwargs):
        self.user = get_current_user()
        self.post_list = get_post_list()
        self.custom_id = make_custom_string_as_id("PostList")
        PostList.objects.prefetch_related().filter(user=self.user).delete()
        
        super(PostList, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        super(FollowRequest, self).delete(*args, **kwargs)

