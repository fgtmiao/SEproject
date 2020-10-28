# SEproject
for 软件工程项目
## 前端修改
* 通过修改se_frontend/src/components下添加vue界面，并在se_frontend/src/router/index.js下修改路由即可导向目标页面，之后在frontend文件夹中执行npm run build（如果初次使用需要npm install安装依赖）检测是否报错后用dist文件夹；
* 参考https://www.cnblogs.com/zhixi/p/9996832.html执行
* 前端组件添加手段：npm i element-ui -S；在se_frontend/src/main.js引入UI样式，即import的后两行+vue.use
* 把build中的ESlint的前端格式检查去掉了，取消了格式检查
## 后端选择
* django，已经做了初始化
## 数据库选择
* 暂定MySQL