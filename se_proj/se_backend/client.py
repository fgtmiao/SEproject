# coding=utf-8
# client.py 模拟发送请求，用于后台调试

import requests
import hashlib
import json
import base64
import hmac


if __name__ == "__main__":

    index_url = 'http://127.0.0.1:8000/index'

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

    # 获取本次登录的secret并创建jwt
    secret_token = json.loads(res.content)['secret']
    header_text = base64.b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).decode()
    payload_text = base64.b64encode(json.dumps({'lia': user_name}).encode()).decode()       # lia: login as
    signature_text = base64.b64encode(hmac.new(secret_token.encode(), (header_text + '.' + payload_text).encode(), digestmod='sha256').digest()).decode()
    jwt = header_text + '.' + payload_text + '.' + signature_text
    print('my jwt token: %s' % jwt)
    jwt = jwt.encode()

    # 2. 模拟发帖
    post_params = {
        'type': 'add_post', 'jwt': jwt,
        'post': json.dumps({'description': '创世帖'})
    }
    res = requests.post(url=index_url, data=post_params)
    print('模拟发帖 返回结果: %s' % res.text)
    postid = json.loads(res.content)['postid']

    # 3. 模拟读取
    post_params = {
        'type': 'view_posts'
    }
    res = requests.post(url=index_url, data=post_params)
    print('模拟读取 返回结果: %s' % res.text)

    # 4. 模拟读取指定的帖子
    post_params = {
        'type': 'view_posts', 'start_inedx': 5, 'post_num': 3
    }
    res = requests.post(url=index_url, data=post_params)
    print('指定读取 返回结果: %s' % res.text)

    # 5. 模拟回复
    post_params = {
        'type': 'comment_post', 'jwt': jwt,
        'reply': json.dumps({'post': postid, 'description': '创世回复'})
    }
    res = requests.post(url=index_url, data=post_params)
    print('模拟回复 返回结果: %s' % (res.text))

    # 6. 退出登录
    post_params = {
        'type': 'signout', 'jwt': jwt,
    }
    res = requests.post(url=index_url, data=post_params)
    print('退出登录 返回结果: %s' % res.text)

    print('client.py backend test finished')
