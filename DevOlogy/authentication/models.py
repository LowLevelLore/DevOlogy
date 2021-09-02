import datetime
import os
from django.utils.functional import cached_property
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import string
import random
from django.contrib.auth.hashers import make_password


id_length = 20

def make_custom_user_id():
    satisfied = False
    while not satisfied:
        custom_string = ''.join(random.choice(string.ascii_uppercase) for _ in range(id_length))
        check_list = list(User.objects.filter(custom_id=custom_string))
        if len(check_list) == 0:
            satisfied = True

    return custom_string

def get_dp_path(instance, filename):
    return instance.get_dp_upload_path(filename)


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, full_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address.')

        if not username:
            raise ValueError('Users must have an username.')

        # if not date_of_birth:
        #     raise ValueError('Users must have date of birth.')

        if not full_name:
            raise ValueError('Users must have full name.')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            full_name=full_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, full_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=email,
            username=username,
            full_name=full_name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    custom_id = models.CharField(max_length=id_length, null=False, blank=False, editable=False, unique=True)
    email = models.EmailField(max_length=240, null=False, blank=False, unique=True)
    username = models.CharField(max_length=200, null=False, blank=False, unique=True)
    full_name = models.CharField(max_length=300, null=False, blank=False)
    display_picture = models.ImageField(upload_to=get_dp_path, null=True, blank=True)
    bio = models.CharField(max_length=1000, default='', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    objects = MyUserManager()

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        if self.custom_id == '' or self.custom_id is None:
            self.custom_id = make_custom_user_id()
        try:
            this = User.objects.get(pk=self.pk)
            if this.display_picture != self.display_picture:
                this.display_picture.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super(User, self).save(*args, **kwargs)

    def get_dp_upload_path(self, filename):

        return f'UserSpecific/{self.email}/DisplayPicture/{str(datetime.datetime.now())}.jpg'

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin or self.is_superuser

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def __str__(self):
        return str(self.email)

    @property
    def get_bio_links(self):
        links = self.bioLinks.all()
        return links

    @property
    def get_user_posts(self):
        posts = self.users_posts.all()
        return posts

    @property
    def get_bio_links_length(self):
        links = list(self.bioLinks.all())
        return len(links)

    @property
    def get_user_posts_length(self):
        posts = list(self.users_posts.all())
        return len(posts)

    @property
    def get_user_likes_on_posts(self):
        likes_on_posts = list(self.user_who_liked_the_post.all())
        return likes_on_posts

    @property
    def get_user_likes_on_comments(self):
        likes_on_comments = list(self.user_who_liked_the_comment.all())
        return likes_on_comments

    @property
    def get_user_followers(self):
        """
        USERS WHO FOLLOW THE PARTICULAR USER
        :return: USER OBJECTS
        """
        followers = [x.user_who_followed for x in list(self.user_who_was_followed.all())]
        return followers

    @property
    def get_user_following(self):
        """
        USERS WHOM THE PARTICULAR USER FOLLOWS
        :return: USER OBJECTS
        """
        following = [x.user_who_was_followed for x in list(self.user_who_followed.all())]
        return following

    @cached_property
    def get_dp_path(self):
        try:
            return self.display_picture.url
        except:
            return '/static/svgs/user.png'

    @property
    def get_no_of_followers(self):
        return len(self.get_user_followers)

    @property
    def get_no_of_following(self):
        return len(self.get_user_following)

    @property
    def get_min_sugg(self):
        following = self.get_user_following
        counter = 0
        min_sugg = []
        for user in following:
            if counter >= 5:
                break
            for user_ in user.get_user_following:
                if counter >= 5:
                    break
                if user_ not in following and user_ != self:
                    min_sugg.append(user_)
                    counter += 1
        if len(min_sugg) < 5:
            min_sugg = [x for x in User.objects.prefetch_related().all()[:4] if (x not in following and x != self)]
        return min_sugg


class InactiveUser(models.Model):
    custom_id = models.CharField(max_length=id_length, null=False, blank=False, editable=False, unique=True)
    email = models.EmailField(max_length=240, null=False, blank=False, unique=False)
    username = models.CharField(max_length=200, null=False, blank=False, unique=False)
    full_name = models.CharField(max_length=300, null=False, blank=False)
    is_active = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    def save(self, *args, **kwargs):
        try_to_match = list(InactiveUser.objects.filter(email=self.email))
        if len(try_to_match) == 0:
            pass
        else:
            for match in try_to_match:
                match.delete()
        if self.custom_id == '' or self.custom_id is None:
                self.custom_id = make_custom_user_id()
        super(InactiveUser, self).save(*args, **kwargs)