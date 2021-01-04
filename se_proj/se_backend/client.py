# coding=utf-8

# client.py 模拟发送请求，用于后台调试

import requests
import hashlib
import json
import base64
import hmac


def main():
    index_url = 'http://127.0.0.1/index'        # when test on server
    userinfo_url = 'http://127.0.0.1/userinfo'        # when test on server

    # 1. 模拟注册
    user_name = '红黑树'
    password_raw = 'this_is_my_psw'

    md5hl = hashlib.md5()
    md5hl.update(password_raw.encode('utf-8'))
    password = md5hl.hexdigest()
    signup_params = {
        'type': 'signup', 'user_name':  user_name, 'password': password
    }
    res = requests.post(url=index_url, data=signup_params)
    print('模拟注册 返回结果: %s' % res.text)

    if not json.loads(res.content)['succ']:
        # 说明帐号可能已经存在了，所以模拟登录
        signup_params = {
            'type': 'signin', 'user_name':  user_name, 'password': password
        }
        res = requests.post(url=index_url, data=signup_params)
        print('模拟登录 返回结果: %s' % res.text)

    jwt = json.loads(res.content)['token']
    print('my jwt token: %s' % jwt)
    jwt = jwt.encode()

    # 2. 模拟获取自己的用户信息
    get_user_info_params = {
        'type': 'get_user_info', 'user_name': '红黑树'
    }
    res = requests.post(url=userinfo_url, data=get_user_info_params)
    print('模拟获取用户信息 返回结果: %s' % res.text)

    # 3. 模拟更换头像
    test_image = open('./fig.jpeg', 'rb')
    # print(test_image)
    change_fig_params = {
        'jwt': jwt, 'type': 'change_user_fig'
    }
    res = requests.post(url=userinfo_url, data=change_fig_params, files={'image': test_image})
    print('模拟更换头像 返回结果: %s' % res.text)

    # 4. 模拟发帖
    post_params = {
        'type': 'add_post', 'jwt': jwt,
        'post[description]': '这是一个有类别信息和位置信息的帖子',
        'post[position]': '',
        'post[animal_class]': 'bird-swan'       # 多级用'-'相连，例如鸟类-天鹅
    }
    res = requests.post(url=index_url, data=post_params)
    print('模拟发帖 返回结果: %s' % res.text)
    postid = json.loads(res.content)['postid']

    # 5. 模拟读取
    post_params = {
        'type': 'view_posts'
    }
    res = requests.post(url=index_url, data=post_params)
    print('模拟读取 返回结果: %s' % res.text)

    # 6. 模拟读取指定的帖子
    post_params = {
        'type': 'view_posts', 'start_index': 5, 'post_num': 3
    }
    res = requests.post(url=index_url, data=post_params)
    print('指定读取 返回结果: %s' % res.text)

    # 7. 模拟根据动物类别检索帖子
    post_params = {
        'type': 'view_posts', 'animal_class': 'bird'    # 只用'bird'类别也能检索到'bird-swan'类别的帖子
    }
    res = requests.post(url=index_url, data=post_params)
    print('动物类别检索帖子 返回结果: %s' % res.text)

    # 8. 模拟根据正文信息检索帖子
    post_params = {
        'type': 'view_posts', 'description': '位置'
    }
    res = requests.post(url=index_url, data=post_params)
    print('正文内容检索帖子 返回结果: %s' % res.text)

    # 9. 模拟根据用户名检索帖子
    post_params = {
        'type': 'view_posts', 'user_name': 'fgtmiao'
    }
    res = requests.post(url=index_url, data=post_params)
    print('作者用户名检索帖子 返回结果: %s' % res.text)

    # 10. 模拟回复
    post_params = {
        'type': 'comment_post', 'jwt': jwt,
        'reply[post]': postid, 'reply[description]': '创世回复'
    }
    res = requests.post(url=index_url, data=post_params)
    print('模拟回复 返回结果: %s' % (res.text))

    # 11. 模拟读取回复
    post_params = {
        'type': 'view_replies', 'pid': postid
    }
    res = requests.post(url=index_url, data=post_params)
    print('模拟读取回复 返回结果: %s' % (res.text))

    # 12. 模拟检索一种类型的动物的最近位置
    post_params = {
        'type': 'get_location', 'animal_class': 'bird-swan'     # 当然用'bird-swan'这个类别全名检索也是可以的
    }
    res = requests.post(url=index_url, data=post_params)
    print('模拟获取位置 返回结果: %s' % (res.text))

    # 13. 退出登录
    post_params = {
        'type': 'signout', 'jwt': jwt,
    }
    res = requests.post(url=index_url, data=post_params)
    print('退出登录 返回结果: %s' % res.text)

    print('client.py backend test finished')


if __name__ == "__main__":
    main()