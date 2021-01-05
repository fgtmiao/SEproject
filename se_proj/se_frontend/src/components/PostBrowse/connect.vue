<template>
<div>
    <el-page-header @back="goBack" content="返回主页">
    </el-page-header>
<span>
本项目为2020年秋季学期软件工程第四小组完成，如有问题请联系1700012824@pku.edu.cn
</span>
</div>
</template>


<script>
  import Qs from 'qs'
  import axios from "axios"

  export default {
    data() {
return{}
    },
    methods:{
              goBack() {
        this.$router.go(-1);
      },
    }
  }
</script>