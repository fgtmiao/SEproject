"""se_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView 

from se_backend import views

urlpatterns = [
    path('api/index', views.requset_index, name='index'),                               # 平台首页
    path('api/userinfo', views.requset_userinfo, name='userinfo'),                      # 个人主页界面
    path('api/baike_content', views.requset_baike_content, name='baike_content'),       # 燕园动物小百科详细页面
]
