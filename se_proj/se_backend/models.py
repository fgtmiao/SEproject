from django.db import models


class User(models.Model):
    uid = models.AutoField('uid', primary_key=True, auto_created=True)
    user_name = models.TextField('user_name')
    password = models.TextField('password')
    user_auth = models.TextField('user_auth', blank=True, null=True)
    user_desc = models.TextField('user_desc', blank=True, null=True)
    user_fig_src = models.TextField('user_fig_src', blank=True, null=True)
    user_title = models.TextField('user_title', blank=True, null=True)
    is_adm = models.BooleanField('is_adm', default=False)
    secret_token = models.TextField('secret_token', blank=True, null=True)
    reg_time = models.IntegerField('reg_time', blank=True, null=True)
    last_login_time = models.IntegerField('last_login_time', blank=True, null=True)

    class Meta:
        db_table = 'user'


class Post(models.Model):
    pid = models.AutoField('pid', primary_key=True, auto_created=True)
    description = models.TextField('description')
    image_src = models.TextField('image_src', blank=True, null=True)
    animal_class = models.TextField('animal_class', blank=True, null=True)
    position = models.TextField('position', blank=True, null=True)
    likes = models.IntegerField('likes', default=0)
    publisher = models.IntegerField('publisher')
    reports = models.IntegerField('reports', blank=True, null=True)
    processed = models.IntegerField('processed', blank=True, null=True)
    timestamp = models.IntegerField('timestamp')

    class Meta:
        db_table = 'post'


class Reply(models.Model):
    rid = models.AutoField('rid', primary_key=True, auto_created=True)
    description = models.TextField('description')
    image_src = models.TextField('image_src', blank=True, null=True)
    publisher = models.IntegerField('publisher')
    post = models.IntegerField('post')
    floor = models.IntegerField('floor')
    reports = models.IntegerField('reports', blank=True, null=True)
    processed = models.IntegerField('processed', blank=True, null=True)
    timestamp = models.IntegerField('timestamp')

    class Meta:
        db_table = 'reply'
