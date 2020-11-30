import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'
import Login from '@/components/SignInUp/login.vue'
import SignUp from '@/components/SignInUp/signup.vue'
import UserInfo from '@/components/UserInfo/userinfo_modify.vue'
import MainPosts from '@/components/PostBrowse/MainPosts.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',//路由和组件
      name: 'Login',
      component: Login
    },
    {
      path:'/signup',
      name:'SignUp',
      component:SignUp
    },
    {
      path:'/userinfo',
      name:'UserInfo',
      component:UserInfo
    },
    {
      path:'/mainposts',
      name:'MainPosts',
      component:MainPosts
    }
  ]
})
