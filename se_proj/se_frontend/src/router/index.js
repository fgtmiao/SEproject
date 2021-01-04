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
import showLocation from "@/components/PostDetail/showLocation.vue"
import searchRes from "@/components/PostBrowse/searchRes.vue"

Vue.use(Router)

export default new Router({
  routes: [{
      path: '/', //路由和组件
      name: 'Login',
      component: Login
    },
    {
      path: '/signup',
      name: 'SignUp',
      component: SignUp
    },
    {
      path: '/mainposts',
      name: 'MainPosts',
      meta: {
        requireauth: true, // 判断是否需要登录
      },
      component: MainPosts
    },
    {
      path: '/postupload',
      name: 'Upload',
      meta: {
        requireauth: true, // 判断是否需要登录
      },
      component: PostUpload
    },
    {
      path: '/postDetail',
      name: 'postDetail',
      meta: {
        requireauth: true, // 判断是否需要登录
      },
      component: PostDetail
    },
    {
      path: '/userinfo',
      name: 'UserInfo',
      meta: {
        requireauth: true, // 判断是否需要登录
      },
      component: UserInfo
    },

    {
      path: '/baike',
      name: 'Baike',
      meta: {
        requireauth: true, // 判断是否需要登录
      },
      component: Baike
    },
    {
      path: '/showLocation',
      name: 'showLocation',
      meta: {
        requireauth: true, // 判断是否需要登录
      },
      component: showLocation
    },
    {
      path: '/searchRes',
      name: 'searchRes',
      meta: {
        requireauth: true, // 判断是否需要登录
      },
      component: searchRes
    },
  ]
})
