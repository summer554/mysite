from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.blog_list, name='blog_list'),
    url(r'^(\d+)/$', views.blog_detail, name='blog_detail'),
    url(r'^blogtype/(\d+)/$', views.blog_with_type, name='blog_with_type'),
    url(r'^date/(\d+)/(\d+)/$', views.blog_with_date, name='blog_with_date'),
]
