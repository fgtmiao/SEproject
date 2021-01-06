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


def get_user_info(request):
    '''
    POST params:
        [optional] uid: int, 想获取的用户的uid
        [optional] user_name: str, 想获取的用户的用户名
    '''
    uid = request.POST.get('uid')
    user_name = request.POST.get('user_name')
    print(uid, user_name)
    try:
        if uid:
            user = User.objects.get(uid=uid)
        elif user_name:
            user = User.objects.get(user_name=user_name)
        else:
            return JsonResponse({'succ': False, 'errmsg': 'uid or user_name required'})
    except django.core.exceptions.ObjectDoesNotExist:
        return JsonResponse({'succ': False, 'errmsg': 'user_name or uid invalid'})
    except django.core.exceptions.MultipleObjectsReturned:
        return JsonResponse({'succ': False, 'errmsg': 'user_name or uid invalid'})

    user_info = {
        'uid': user.uid, 'user_name': user.user_name, 'user_fig': user.user_fig_src,
        'user_desc': user.user_desc, 'user_title': user.user_title, 'is_adm': user.is_adm
    }
    return JsonResponse({'succ': True, 'user_info': user_info})


def change_user_fig(request, payload):
    '''
    POST params:
        [required] jwt: str, base64 encoded json web token
        [required] image: bin
    '''

    user = User.objects.get(user_name=payload['lia'])

    # 获取并存储图片
    image_dict = list(request.FILES.items())
    if not image_dict:
        return JsonResponse({'succ': False, 'errmsg': 'image required'})

    for (k, v) in image_dict:
        image_data = request.FILES.getlist(k)
        print('image_data', image_data)
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
        break

    user.user_fig_src = os.path.join('http://' + ALLOWED_HOSTS[0], 'images', image_fname)
    user.save()
    return JsonResponse({'succ': True, 'user_fig': user.user_fig_src})
