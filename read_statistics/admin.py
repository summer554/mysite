from django.contrib import admin
from .models import ReadNum, ReadDetail

@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ['pk', 'read_num', 'content_object']
    list_filter = ['read_num']
    search_fields = ['read_num']
    list_per_page = 3

@admin.register(ReadDetail)
class ReadDetailAdmin(admin.ModelAdmin):
    list_display = ['pk', 'date', 'read_num', 'content_object']
    list_filter = ['date']
    search_fields = ['date']
    list_per_page = 3