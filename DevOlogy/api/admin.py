from django.contrib import admin
from .models import ProfilePostList

# Register your models here.

class ProfilePostListAdmin(admin.ModelAdmin):
    list_display = ('custom_id', 'user', 'updated_on')

admin.site.register(ProfilePostList, ProfilePostListAdmin)