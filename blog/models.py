from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum, ReadNumExtend, ReadDetail
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse

class BlogType(models.Model):
    type_name = models.CharField(max_length=15)
    def __str__(self):           #相当于toString方法
        return self.type_name

class Blog(models.Model, ReadNumExtend):
    title = models.CharField(max_length=30)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    read_details = GenericRelation(ReadDetail) #关联到全部的ReadDetail
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Blog: %s>" % self.title

    def get_url(self):
        return reverse('blog_detail', args=[self.pk])

    def get_email(self):
        return self.author.email

    #创建的类按照创建时间排序
    class Meta:
        ordering = ['-created_time']

