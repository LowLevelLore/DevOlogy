from django.contrib import admin
from .models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    fields = ('email', 'password', 'username', 'full_name', 'bio', 'display_picture')
    list_display = ('email', 'username')

admin.site.register(User, UserAdmin)
