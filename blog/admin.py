from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Post, Comment


# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'gender', 'interest', 'phone_number', 'first_name', 'last_name']
    list_filter = ['interest']
    search_fields = ('interest',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'created', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


admin.site.site_header = 'My Blog Site Admin'

'''
from django.contrib import admin
from .models import CustomUser
# Register your models here.
admin.site.site_header = 'My Blog Site'
admin.site.register(CustomUser)
'''

'''
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'gender', 'interest', 'phone_number', 'first_name', 'last_name']
    list_filter = ['interest']
    search_fields = ('interest',)


admin.site.site_header = 'My Blog Site'

'''