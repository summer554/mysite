from django.shortcuts import render
from .models import LikeCount, LikeRecord
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
def ErrorResponse(code, message):
    data = {}
    data['status'] = 'error'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)

def SuccessResponse(liked_num):
    data = {}
    data['status'] = 'success'
    data['liked_num'] = liked_num
    return JsonResponse(data)

def like_change(request):
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400, '请登录')
    #获取应得的数据
    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))
    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401, '对象不存在')
    is_like = request.GET.get('is_like')

    if is_like == 'true':
        #要点赞
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if created:
            #未点赞过，进行点赞
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.liked_num = like_count.liked_num + 1
            like_count.save()
            return SuccessResponse(like_count.liked_num)
        else:
            #已点赞过，不能重复点赞
            return ErrorResponse(402, '已点赞')
    else:
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            #有点赞，取消点赞
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            #点赞总数减一
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                like_count.liked_num = like_count.liked_num - 1
                like_count.save()
                return SuccessResponse(like_count.liked_num)
            else:
                return ErrorResponse(404, '数据错误')
        else:
            #没有点赞过，不能取消
            return ErrorResponse(403, '没有点赞')
