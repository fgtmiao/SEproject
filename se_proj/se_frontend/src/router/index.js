import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'
import Login from '@/components/SignInUp/login.vue'
import SignUp from '@/components/SignInUp/signup.vue'

import MainPosts from '@/components/PostBrowse/MainPosts.vue'
import PostUpload from '@/components/PostUpload/Upload.vue'
import PostDetail from '@/components/PostDetail/Post.vue'

import UserInfo from "@/components/UserInfo/userinfo_display.vue"
// import UserInfo from "@/components/UserInfo/test.vue"

import Baike from "@/components/baike/baike.vue"

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
      path:'/mainposts',
      name:'MainPosts',
      component:MainPosts
    },
    {
      path:'/postupload',
      name:'Upload',
      component:PostUpload
    },
    {
      path:'/postDetail',
      name:'postDetail',
      component:PostDetail
    },
    {
      path:'/userinfo',
      name:'UserInfo',
      component:UserInfo
    },

    {
      path:'/baike',
      name:'Baike',
      component:Baike
    },
  ]
})
