from re import S
from django.db import models
from core.models import Post, id_length
from authentication.models import User
import random
import string
import json
from crum import get_current_user
# Create your models here.

def get_profile_post_list(user):
    x_ = list(Post.objects.prefetch_related().filter(user=user).order_by('-posted_on'))
    response = {}
    for post in x_:
        response[post.custom_id] = {
            "custom_id": post.custom_id,
            "caption": post.caption,
            "picture": post.picture.url,
            "user": post.user.username,
            "likes": post.get_post_likes_length
        }
    
    return json.dumps(response)

def make_custom_string_as_id():
    satisfied = False
    while not satisfied:
        custom_string = ''.join(random.choice(
            string.ascii_uppercase) for _ in range(id_length))
        try:
            (ProfilePostList.objects.prefetch_related().get(custom_id=custom_string))
        except:
            satisfied = True

    return custom_string

class ProfilePostList(models.Model):
    custom_id = models.CharField(
        max_length=id_length, null=False, editable=False, blank=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    spec = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profilespec')
    updated_on = models.DateTimeField(auto_now_add=True)
    profilePostList = models.JSONField()

    def save(self, *args, **kwargs):
        self.profilePostList = get_profile_post_list(self.user)
        self.spec = get_current_user()
        self.custom_id = make_custom_string_as_id()
        ProfilePostList.objects.prefetch_related().filter(user=self.user).delete()
        super(ProfilePostList, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(ProfilePostList, self).delete(*args, **kwargs)