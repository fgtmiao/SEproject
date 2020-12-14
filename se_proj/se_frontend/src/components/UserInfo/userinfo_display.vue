<template>
<div>
<!--header here-->
    <div class="allbox">
    <!--div class = "mainheader">
    <el-card class = "headercard">
        <el-divider><span class="headertext">PASS小动物照片分享平台</span></el-divider>
        <div>
        <el-input placeholder="请输入搜索内容" v-model="searchbar.input" autocomplete="off" class="searchClass">
            <el-button slot="append" icon="el-icon-search" @click="searchF()"></el-button>
        </el-input>
        </div>

    </el-card>
    </div-->
  <el-page-header @back="goBack" content="发布帖子">
</el-page-header>
      <div class ="userInfoCard">
        <el-card>
        <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"></el-avatar>
        <span>this is username</span>
        <el-button v-if='ismine' @click='ChangeAvater()'>修改头像</el-button>
        </el-card>
      </div>
        <!--all post here 就直接堆一个他的帖子>
        <div class="cardlist">
        <el-card class="">
        </el-card-->
 
  <!--他的帖子-->
  <span v-if='ismine'>我的帖子</span>
  <span v-else>TA的帖子</span>
    <div class="CardList">
    <el-row class="cardrow">
      <div  v-for="(post,index) in posts" :key='post.index' >
        <el-card class = "Showcard"  :body-style="{ padding:'0px' }"  >
        <div @click="postDetail(post.postID)">
        <div style="padding: 14px;" >
        <div class="userHeader">
            <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"></el-avatar>
            <span>this is username</span>
        </div>
            <span class="PostDescription">{{post.postDescrip}}</span>
            <div class="bottom clearfix">
            <!--el-button type="text" class="button">帖子详情</el-button-->
            </div>
        </div>
        <!--选择每个帖子预先显示一张图，详情之后再显示其他图-->

            <div class="covers" >
                <!--img :src="img.src" width="90%" class="min" alt=""-->
                <li class="imgbox"><img class="image" :src="post.images[0].src"/></li>
            </div>
        <time class="time">{{ currentDate }}</time>
        <!--icon&location here-->
        <i class="el-icon-location-information"></i>
        <i class= "el-icon-picture-outline"></i>
        </div>
        </el-card>
      </div>
    <!--/el-col-->
    </el-row>
    </div>
     </div>
    </div>
</div>
</template>

<script>
//for header
export default {
  data() {
    
    return {
      ismine:true,
      activeIndex2: '1',
      currentDate:new Date(),
      searchbar:{
      input: '',
      },
      posts:[
      {
        "postID":"123",
        "postDescrip":"asdadads",
        "images":[
          {
          "src":require('../../assets/Jhin.jpg'),
          }
        ]
        },
      ]
    }
  },
  mounted(){
    this.validateMine();
  },
  methods:{
    validateMine(){
      this.ismine=false;
    },
      searchF()
      {
          //search for
        console.log(this.searchbar.input)
        
      },
      goBack(){

      this.$router.go(-1);
      },

ChangeAvater(){
  console.log("want to change avater");
},

      handleSelect(key, keyPath) {
        console.log(key, keyPath);
        if(key=="4"){
          this.$router.push({path:'/userinfo', query:{"userID":"this is userid"} })
        }
      } 
  }
}
</script>

<style acoped>
.headercard{
  padding-top: 30px;
  border-radius: 0px;
}
.headertext{
  color:#101010;
  font-size:30px;
}
.allbox{
  background-image:url("../../assets/bg_new.jpg");
  background-size: contain;
  height:100%;
  background-position: 400px 0px;
  background-repeat: no-repeat;
  background-attachment: fixed;
}

.searchClass{
  // position:fixed;
  border: 1px solid #c5c5c5;
  border-radius: 20px;
  background: #f4f4f4;
  margin-bottom:10px;
}
.searchClass .el-input-group__prepend {
  border: none;
  background-color: transparent;
  // padding: 0 10px 0 30px;
}
.searchClass .el-input-group__append {
  border: none;
  background-color: transparent;
}
.searchClass .el-input__inner {
  height: 36px;
  line-height: 36px;
  border: none;
  background-color: transparent;
}
.searchClass .el-icon-search{
  font-size: 16px;
}

.searchClass .line {
  width: 1px;
  height: 26px;
  background-color: #c5c5c5;
  margin-left: 14px;
}
.searchClass:hover{
  border: 1px solid #D5E3E8;
  background: #fff;
}
.searchClass:hover .line {
  background-color: #D5E3E8;
}
.searchClass:hover .el-icon-search{
  color: #409eff;
  font-size: 16px;
}

//for user
.userInfoCard{
  margin:50px;
  padding:50px;  
}
//for posts
.minePosts{

}
</style>