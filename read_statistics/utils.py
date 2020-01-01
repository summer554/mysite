from django.contrib.contenttypes.models import ContentType
from .models import ReadNum, ReadDetail
from django.utils import timezone
from django.db.models import Sum
import datetime
def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)
    if not request.COOKIES.get(key):
        #get_or_create
        if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
            # 存在记录
            readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        else:
            readnum = ReadNum(content_type=ct, object_id=obj.pk)
        readnum.read_num = readnum.read_num + 1
        readnum.save()
        #当天阅读数加1
        date = timezone.now().date()
        if ReadDetail.objects.filter(content_type=ct, object_id=obj.pk, date=date).count():
            readDetail = ReadDetail.objects.filter(content_type=ct, object_id=obj.pk, date=date)
        else:
            readDetail = ReadDetail(content_type=ct, object_id=obj.pk, date=date)
        readDetail.read_num = readDetail.read_num + 1
        readDetail.save()
    return key

#获取前七天月度数据
def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)  # 若前面为false则结果为0
    return dates, read_nums

#获取当前热门博客
def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    #将查询集结果按照read_num倒序排序
    return read_details[:3]

def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    # 将查询集结果按照read_num倒序排序
    return read_details[:3]


