# coding=utf-8

import json
import hmac
import base64

import django
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from se_backend.models import User, Post, Reply

from se_backend import index


@csrf_exempt
def requset_index(request):
    if 'type' not in request.POST:
        return HttpResponse('Hello World from page index!')

    elif request.POST['type'] == 'signin':
        return index.signin(request)

    elif request.POST['type'] == 'signup':
        return index.signup(request)

    elif request.POST['type'] == 'signout':
        payload = verify_jwt(request.POST['jwt'])
        if payload:
            return index.signout(request, payload)

    elif request.POST['type'] == 'view_posts':
        return index.view_posts(request)

    elif request.POST['type'] == 'view_replies':
        return index.view_replies(request)

    elif request.POST['type'] == 'add_post':
        payload = verify_jwt(request.POST['jwt'])
        if payload:
            return index.add_post(request, payload)

    elif request.POST['type'] == 'comment_post':
        payload = verify_jwt(request.POST['jwt'])
        if payload:
            return index.comment_post(request, payload)

    else:
        return JsonResponse({'succ': False, 'errmsg': 'undefined request'})
    return JsonResponse({'succ': False, 'errmsg': 'authentication failed'})


@csrf_exempt
def requset_userinfo(request):
    return HttpResponse('Hello World from page userinfo!')


@csrf_exempt
def requset_baike_content(request):
    return HttpResponse('Hello World from page baike_content!')


def verify_jwt(jwt: str):
    '''
    params:
        jwt: header.payload.signature字符串
    return:
        解码后的payload json对象，若jwt不合法则返回None
    '''
    header_text, payload_text, signature_text = jwt.split('.')
    payload = json.loads(base64.b64decode(payload_text.encode()).decode())
    try:
        user = User.objects.get(user_name=payload.get('lia'))
    except django.core.exceptions.ObjectDoesNotExist:
        return None
    except django.core.exceptions.MultipleObjectsReturned:
        return None

    secret_token = user.secret_token
    server_signature = base64.b64encode(hmac.new(secret_token.encode(), (header_text + '.' + payload_text).encode(), digestmod='sha256').digest()).decode()
    if server_signature != signature_text:
        return None
    return payload
