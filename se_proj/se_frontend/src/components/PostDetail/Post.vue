<template>
<div>
<!--header-->
<el-page-header @back="goBack" content="帖子详情">
</el-page-header>
<!--post detail-->
<el-card class = "Postcard"  :body-style="{ padding: '30px' }"  >
        <!--发帖人-->

        <div style="padding: 14px;" >
            <span class="PostDescription">{{post.postDescrip}}</span>
            <div class="bottom clearfix">
            <time class="time">{{ currentDate }}</time>
            <!--el-button type="text" class="button">帖子详情</el-button-->
            </div>
        </div>
        <!--九宫格-->
            <div class="covers" >
                <img class="image" :src="post.images[0].src"/>
            </div>
</el-card>
<!--comment here-->
</div>
</template>

<script>

export default {
  data() {
    
    return {
    postDetail:{
        "postID":"",
        "images":[
            {"src":require('../../assets/Jhin.jpg')}
        ]
    }
    }
  },
  methods:{
      goBack(){
        this.$router.push({path:'/mainposts', query:{} })
      }
  }
}
</script>

<style acoped>

</style>