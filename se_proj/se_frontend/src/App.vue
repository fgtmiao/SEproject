<template>
  <div id="app">
    <!--img src="./assets/logo.png"加入组件渲染出口
    mainjs Appvue routers Login,访问http://localhost:xxxx/#/login即可-->
    
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
