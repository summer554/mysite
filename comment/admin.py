from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'content_object', 'text', 'comment_time', 'user']
    list_filter = ['user', 'text']
    search_fields = ['user', 'text']
    list_per_page = 3
