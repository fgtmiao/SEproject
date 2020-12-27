# SEproject
for 软件工程项目
## 前端修改
* 前端本地运行方式：进入se_frontend文件夹，执行命令npm run dev打开浏览器查看对应端口即可，初次运行可能需要npm run install等
* 前端编写方法：在se_frontend/src/components中添加页面并在se_frontend/router/index.js中添加路由
* 通过修改se_frontend/src/components下添加vue界面，并在se_frontend/src/router/index.js下修改路由即可导向目标页面，之后在frontend文件夹中执行npm run build（如果初次使用需要npm install安装依赖）检测是否报错后用dist文件夹；
* 参考https://www.cnblogs.com/zhixi/p/9996832.html执行
* 前端组件添加手段：npm i element-ui -S；在se_frontend/src/main.js引入UI样式，即import的后两行+vue.use
* 把build中的ESlint的前端格式检查去掉了，取消了格式检查
## 后端选择
* django，已经做了初始化
## 数据库选择
* 暂定MySQL


# 工程运行方法
进入工程目录（即`manage.py`所在的目录） `cd se_proj`

安装所需的python包 `pip install django pymysql requests`

`cp ./se_proj/config.sample.py ./se_proj/config.py` 并在`config.py`中修改你的数据库配置

在mysql中创建你在`config.py`中`NAME`字段写下的database。例如在mysql中运行：`CREATE DATABASE passbase DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`

初始化数据库 `python manage.py makemigrations se_backend; python manage.py migrate`

启动服务 `python manage.py runserver`


# 后端测试方法
运行后端测试样例 `python ./se_backend/client.py`

运行前请将`se_backend/client.py`中`index_url`修改为你的后端服务实际所在的地址。
