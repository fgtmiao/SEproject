// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
/* 引入组件包 */
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import ElImageViewer from "element-ui/packages/image/src/image-viewer";
Vue.config.productionTip = false
//设置axios
Vue.prototype.$axios = axios
axios.defaults.baseURL = '/api' //每次发送的请求都会带一个/api的前缀

Vue.use(ElementUI)
Vue.use(ElImageViewer)


/*路由守卫*/
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireauth)) { // 判断该路由是否需要登录权限
    //  console.log('需要登录');
    if (localStorage.token) { //登录存入的token是否存在，为啥一直有token啊
      next();
    } else {
      next({
        path: '/',
        query: {
          redirect: to.fullpath
        } // 将跳转的路由path作为参数，登录成功后跳转到该路由
      })
    }
  } else {
    next();
  }
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: {
    App
  },
  template: '<App/>'
})
