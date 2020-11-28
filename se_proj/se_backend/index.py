# coding=utf-8

import time
import random
import string
import json

import django
from django.db import models
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db.models import F
from se_backend.models import User, Post, Reply


def signin(request):
    '''
    POST params:
        [required] user_name: str
        [required] password: str
    '''

    try:
        user = User.objects.get(user_name=request.POST.get('user_name'), password=request.POST.get('password'))
    except django.core.exceptions.ObjectDoesNotExist:
        return JsonResponse({'succ': False, 'errmsg': 'user_name or password invalid'})
    except django.core.exceptions.MultipleObjectsReturned:
        return JsonResponse({'succ': False, 'errmsg': 'user_name or password invalid'})

    secret_token = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    user.secret_token = secret_token
    user.last_login_time = int(time.time())
    user.save()

    return JsonResponse({'succ': True, 'secret': secret_token})


def signup(request):
    '''
    POST params:
        [required] user_name: str
        [required] password: str
    '''
    # 检查用户名是否已经被注册过
    result = User.objects.filter(user_name=request.POST.get('user_name'))
    print(len(result))
    if len(result) != 0:
        return JsonResponse({'succ': False, 'errmsg': 'user_name already exists'})
    user = User()
    user.user_name = request.POST.get('user_name')
    user.password = request.POST.get('password')
    user.reg_time = int(time.time())
    user.save()

    # 注册完成后登录
    return signin(request)


def signout(request, payload):
    '''
    POST params:
        [required] jwt: str, base64 encoded json web token
    '''
    user = User.objects.get(user_name=payload['lia'])
    user.secret_token = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    user.save()
    return JsonResponse({'succ': True})


def view_posts(request):
    '''
    POST params:
        [optional] start_index: int, 要获取的post中pid最大的一个。默认为数据库所有post中最大的pid
        [optional] post_num: int, 要获取的帖子数量。默认为20，不能大于100
        [optional] animal_class: str
        [optional] position: str
    '''
    start_index = int(request.POST.get('start_index', default=-1))
    post_num = int(request.POST.get('post_num', default=20))
    animal_class = request.POST.get('animal_class')
    position = request.POST.get('position')
    if post_num > 100:
        return JsonResponse({'succ': False, 'errmsg': 'requset post_num should not be larger than 100'})
    if start_index == -1:
        start_index = Post.objects.order_by(F('pid').desc())[0].pid
    post_query_set = Post.objects.filter(pid__lte=start_index)
    if animal_class:
        post_query_set = post_query_set.filter(animal_class__startswith=animal_class)
    if position:
        # 目前通过position字符串精确匹配实现potision的筛选，将来可能通过坐标比较等更有实际价值的方式
        post_query_set = post_query_set.filter(position=position)
    post_query_set = post_query_set.order_by(F('pid').desc())

    # 从query_set中取出前n个结果并返回
    post_dicts = []
    for post in post_query_set:
        post_dicts.append(model_to_dict(post))
        if len(post_dicts) >= post_num:
            break
    return JsonResponse({'succ': True, 'post_info_list': post_dicts})


def add_post(request, payload):
    '''
    POST params:
        [required] jwt: str, base64 encoded json web token
        [required] post: dict
        [required] post.description: str
        [optional] post.image_src: str
        [optional] post.animal_class: str
        [optional] post.position: str
    '''
    post_json = request.POST.get('post')
    if not post_json:
        return JsonResponse({'succ': False, 'errmsg': 'post required'})
    post_dict = json.loads(post_json)

    description = post_dict.get('description')
    image_src = post_dict.get('image_src')
    animal_class = post_dict.get('animal_class')
    position = post_dict.get('position')
    publisher = User.objects.get(user_name=payload['lia']).uid
    if not description:
        return JsonResponse({'succ': False, 'errmsg': 'post description required'})

    post = Post()
    post.publisher = publisher
    post.description = description
    post.image_src = image_src
    post.animal_class = animal_class
    post.position = position
    post.timestamp = int(time.time())
    post.save()
    return JsonResponse({'succ': True, 'postid': post.pid})


def comment_post(request, payload):
    '''
    POST params:
        [required] jwt: str, basr64 encoded json web token
        [required] reply: dict
        [required] reply.post: int, 要回复的帖子的pid
        [required] reply.description: str
        [optional] reply.image_src: str
    '''
    reply_json = request.POST.get('reply')
    if not reply_json:
        return JsonResponse({'succ': False, 'errmsg': 'reply required'})
    reply_dict = json.loads(reply_json)

    pid = reply_dict.get('post')
    description = reply_dict.get('description')
    image_src = reply_dict.get('image_src')
    publisher = User.objects.get(user_name=payload['lia']).uid
    if not description:
        return JsonResponse({'succ': False, 'errmsg': 'reply description required'})
    if not pid:
        return JsonResponse({'succ': False, 'errmsg': 'reply post id required'})

    replies = Reply.objects.filter(post=pid).order_by(F('floor').desc())
    if len(replies) == 0:
        reply_floor = 0
    else:
        reply_floor = replies[0].floor + 1

    reply = Reply()
    reply.publisher = publisher
    reply.description = description
    reply.image_src = image_src
    reply.post = pid
    reply.floor = reply_floor
    reply.timestamp = int(time.time())
    reply.save()
    return JsonResponse({'succ': True, 'floor': reply_floor})
