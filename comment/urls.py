from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^update_comment/$', views.update_comment, name='update_comment'),
]