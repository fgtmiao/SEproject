# coding=utf-8

import os
import time
import random
import string
import json
import hmac
import base64

import django
from django.db import models
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db.models import F
from se_backend.models import User, Post, Reply
from se_proj.settings import ALLOWED_HOSTS, image_base_folder
from se_backend import userinfo


def build_jwt_token(secret, user_name):
    header_text = base64.b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).decode()
    payload_text = base64.b64encode(json.dumps({'lia': user_name}).encode()).decode()       # lia: login as
    signature_text = base64.b64encode(hmac.new(secret.encode(), (header_text + '.' + payload_text).encode(), digestmod='sha256').digest()).decode()
    jwt = header_text + '.' + payload_text + '.' + signature_text
    return jwt


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
    jwt_token = build_jwt_token(secret_token, request.POST.get('user_name'))
    user_info = {
        'uid': user.uid, 'user_name': user.user_name, 'user_fig': user.user_fig_src,
        'user_desc': user.user_desc, 'user_title': user.user_title, 'is_adm': user.is_adm
    }
    return JsonResponse({'succ': True, 'token': jwt_token, 'user_info': user_info})


def signup(request):
    '''
    POST params:
        [required] user_name: str
        [required] password: str
    '''
    # 检查用户名是否已经被注册过
    result = User.objects.filter(user_name=request.POST.get('user_name'))
    if len(result) != 0:
        return JsonResponse({'succ': False, 'errmsg': 'user_name already exists'})

    # 添加新用户信息
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
    # 生成一个随机secret覆盖原来的secret
    user.secret_token = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    user.save()
    return JsonResponse({'succ': True})


def view_posts(request):
    '''
    POST params:
        [optional] start_index: int, 要获取的post中pid最大的一个。默认为数据库所有post中最大的pid
        [optional] post_num: int, 要获取的帖子数量。默认为20，不能大于100

        以下字段如果同时使用多个，则使用and布尔逻辑检索，返回符合所有字段要求的记录
        [optional] animal_class: str, 根据动物类型检索
        [optional] position: str, 根据地理位置检索，目前的实现方式是字符串匹配，如果数据库中的地址包含本字段的内容则返回该帖子
        [optional] description: str, 根据帖子内容检索
        [optional] user_name: str, 根据发帖人的用户名检索
        [optional] uid: int, 根据发帖人的uid检索
    '''
    start_index = int(request.POST.get('start_index', default=-1))
    post_num = int(request.POST.get('post_num', default=20))
    animal_class = request.POST.get('animal_class')
    position = request.POST.get('position')
    description = request.POST.get('description')
    user_name = request.POST.get('user_name')
    uid = int(request.POST.get('uid', default=-1))

    if post_num > 100:
        return JsonResponse({'succ': False, 'errmsg': 'requset post_num should not be larger than 100'})
    if start_index == -1:
        start_index = Post.objects.order_by(F('pid').desc())[0].pid
    post_query_set = Post.objects.filter(pid__lte=start_index)
    if animal_class:
        post_query_set = post_query_set.filter(animal_class__startswith=animal_class)
    if position:
        post_query_set = post_query_set.filter(position=position)
    if description:
        post_query_set = post_query_set.filter(description__contains=description)
    if user_name:
        try:
            user = User.objects.get(user_name=user_name)
            post_query_set = post_query_set.filter(publisher=user.uid)
        except (django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.MultipleObjectsReturned):
            print('user_name %s does not exist' % user_name)
    if uid != -1:
        post_query_set = post_query_set.filter(publisher=uid)

    post_query_set = post_query_set.order_by(F('pid').desc())

    # 从query_set中取出前n个结果并返回
    post_dicts = []
    for post in post_query_set:
        post_dicts.append(model_to_dict(post))
        if len(post_dicts) >= post_num:
            break

    # 将结果中的publisher从uid转换为user_name
    uid_to_user = dict()
    uids = set([post_dict['publisher'] for post_dict in post_dicts])
    for uid in uids:
        try:
            publisher_user = User.objects.get(uid=uid)
            uid_to_user[uid] = {'user_name': publisher_user.user_name, 'user_fig': publisher_user.user_fig_src}
        except Exception:
            uid_to_user[uid] = ''

    for i, post_dict in enumerate(post_dicts):
        # 添加作者的名称和头像
        post_dicts[i]['user_name'] = uid_to_user[post_dict['publisher']]['user_name']
        post_dicts[i]['user_fig'] = uid_to_user[post_dict['publisher']]['user_fig']
        # 处理图片url
        if post_dict['image_src']:
            post_dicts[i]['image_src'] = ','.join([os.path.join('http://' + ALLOWED_HOSTS[0], 'images', url) for url in post_dict['image_src'].split(',')])
    return JsonResponse({'succ': True, 'post_info_list': post_dicts})


def view_replies(request):
    '''
    POST params:
        [requried] pid: int, 要查看哪个帖子的回复
    '''
    pid = int(request.POST.get('pid', default=-1))
    reply_query_set = Reply.objects.filter(post=pid)
    reply_dicts = []
    for reply in reply_query_set:
        reply_dicts.append(model_to_dict(reply))

    # 将结果中的publisher从uid转换为user_name
    uid_to_user = dict()
    uids = set([reply_dict['publisher'] for reply_dict in reply_dicts])
    for uid in uids:
        try:
            publisher_user = User.objects.get(uid=uid)
            uid_to_user[uid] = {'user_name': publisher_user.user_name, 'user_fig': publisher_user.user_fig_src}
        except Exception:
            uid_to_user[uid] = ''

    for i, reply_dict in enumerate(reply_dicts):
        reply_dicts[i]['user_name'] = uid_to_user[reply_dict['publisher']]['user_name']
        reply_dicts[i]['user_fig'] = uid_to_user[reply_dict['publisher']]['user_fig']
    return JsonResponse({'succ': True, 'reply_info_list': reply_dicts})


def add_post(request, payload):
    '''
    POST params:
        [required] jwt: str, base64 encoded json web token
        [required] post: dict
        [required] post[description]: str
        [optional] post[image]: bin
        [optional] post[animal_class]: str
        [optional] post[position]: str "[x],[y]". e.g.: "0.123,5.345"
    '''

    description = request.POST.get('post[description]')
    animal_class = request.POST.get('post[animal_class]')
    position = request.POST.get('post[position]')
    publisher = User.objects.get(user_name=payload['lia']).uid
    if not description:
        return JsonResponse({'succ': False, 'errmsg': 'post description required'})

    # 获取并存储图片
    image_dict = request.FILES.items()
    if image_dict:
        image_urls = []
        for (k, v) in image_dict:
            image_data = request.FILES.getlist(k)
            for image in image_data:
                existed_images = os.listdir(image_base_folder)
                image_fname = ''.join(random.sample(string.ascii_letters + string.digits, 32)) + '.jpeg'
                while image_fname in existed_images:
                    image_fname = ''.join(random.sample(string.ascii_letters + string.digits, 32)) + '.jpeg'  # 生成随机文件名
                image_fd = open(os.path.join(image_base_folder, image_fname), 'wb')
                if image.multiple_chunks():
                    for content in image.chunks():
                        image_fd.write(content)
                else:
                    image_fd.write(image.read())
                image_urls.append(image_fname)
    image_urls = ','.join(image_urls)

    post = Post()
    post.publisher = publisher
    post.description = description
    post.image_src = image_urls
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
        [required] reply[post]: int, 要回复的帖子的pid
        [required] reply[description]: str
        [optional] reply[image_src]: str
    '''

    pid = request.POST.get('reply[post]')
    description = request.POST.get('reply[description]')
    image_src = request.POST.get('reply[image_src]')

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


def get_location(request):
    '''
    POST params:
        [required] animal_class: str
        [optional] pos_num: int, 要返回的坐标数量，返回该动物类别最近发布的pos_num个有坐标信息的帖子中的坐标。默认为10
    '''

    animal_class = request.POST.get('animal_class')
    pos_num = int(request.POST.get('pos_num', default=-1))

    if not animal_class:
        return JsonResponse({'succ': False, 'errmsg': 'animal class required'})
    if pos_num == -1:
        pos_num = 10

    post_query_set = Post.objects.filter(animal_class__startswith=animal_class)
    post_query_set = post_query_set.exclude(position__isnull=True).exclude(position__exact='')
    post_query_set = post_query_set.order_by(F('pid').desc())

    # 从query_set中取出前n个结果并返回帖子的位置信息和pid
    post_dicts = []
    for post in post_query_set:
        post_dicts.append(model_to_dict(post))
        if len(post_dicts) >= pos_num:
            break
    pos, pid = [], []
    for post_dict in post_dicts:
        pos.append(post_dict['position'])
        pid.append(post_dict['pid'])
    return JsonResponse({'succ': True, 'pos': pos, 'pid': pid})
