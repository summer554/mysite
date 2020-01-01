from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from django.utils import timezone


#创建单独的应用用于计数 相当于是先根据字段先找到对应的模型 再根据id找到对应的记录
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    #固定应用 contenttype指向的是模型名字 这里的外键就表示指向对应的模型
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

#封装抽象出的类
class ReadNumExtend():
    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:  #如果对象不存在就返回0
            return 0

#创建一个模型用于存储每天阅读数量的明细信息
class ReadDetail(models.Model):
    date = models.DateField(default=timezone.now)
    read_num = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')