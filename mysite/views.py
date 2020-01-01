import datetime
from django.utils import timezone
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data
from blog.models import Blog
from django.db.models import Sum
from django.core.cache import cache

def get_seven_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects \
        .filter(read_details__date__lt=today, read_details__date__gte=date) \
        .values('title', 'id') \
        .annotate(read_num_sum=Sum('read_details__read_num')) \
        .order_by('-read_num_sum')
    return blogs
def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)

    today_hot_data = get_today_hot_data(blog_content_type)

    yesterday_hot_data = get_yesterday_hot_data(blog_content_type)

    #获取七天热门缓存数据
    seven_hot_data = cache.get('seven_hot_data')
    if seven_hot_data is None:
        seven_hot_data = get_seven_days_hot_blogs()
        cache.set('seven_hot_data', seven_hot_data, 3600)

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = today_hot_data
    context['yesterday_hot_data'] = yesterday_hot_data
    context['seven_hot_data'] = seven_hot_data
    return render(request, 'home.html', context)
