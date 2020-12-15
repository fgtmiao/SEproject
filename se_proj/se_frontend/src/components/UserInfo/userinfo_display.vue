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
      <el-page-header @back="goBack" content="个人主页">
      </el-page-header>
      <div class ="userInfoCard">
        <el-card>
        <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"></el-avatar>
        <span>{{tmp_username}}</span>

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

              <div class="imgcovers" >
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
</template>

<script>
//for header
export default {
  data() {
    
    return {
      ismine:true,
      tmp_username:localStorage.getItem('tmp_username'),
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
      //test 同一个人
      // this.ismine=false;
      const tmp_username=localStorage.getItem('tmp_username');
      const fromname = this.$route.query.username;
      this.ismine = (tmp_username==fromname);
      this.tmp_username = fromname;
    },
      searchF()
      {
          //search for
        console.log(this.searchbar.input)
        
      },
      goBack(){

      this.$router.go(-1);
      },
      postDetail(Inp){
        this.$router.push({path:'/postDetail', query:{"postID":Inp} })
      },
    ChangeAvater(){
    console.log("want to change avater");
    },

  }
}
</script>

<style scoped>

.allbox{
  background-image:url("../../assets/bg_new.jpg");
  background-size: contain;
  height:100%;
  width:100%;
  background-position: 400px 0px;
  background-repeat: no-repeat;
  position:fixed;
}

  .line{
    padding :20px
  }
  .time {
    font-size: 13px;
    color: #999;
  }
//for user
.userInfoCard{
}
//for posts
.minePosts{

}
.CardList{
.cardrow{
position:center center;
}  
}

.Showcard{
  width: 60%;
  height: 70%;
  margin-top: 13px;
}
.imgbox{
    font-size: 0;
    vertical-align: middle;
    justify-content:center;
    position: center center;
    display: inline-block;
    width: 500px;
    height: 300px;
    line-height: 240px;
    text-align: center;
    // outline: 1px solid #000;
    margin-bottom:10px
}
.imgbox img{
    max-height: 100%;
    max-width: 100%;
    vertical-align: middle;

}

</style>