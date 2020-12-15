<template>
<div>
<!--header父子组件太容易出bug，还是老老实实复制粘贴
首页分类搜索结果都在这个界面做-->

  <div class="allbox">
    <div class = "mainheader">
    <!--el-card class = "headercard"  :body-style="{ padding: '30px'}"-->
    <el-card class = "headercard">
      <el-divider><span class="headertext">PASS小动物照片分享平台</span></el-divider>
      <div>
        <el-input placeholder="请输入搜索帖子内容" v-model="searchbar.input" autocomplete="off" class="searchClass">
          <el-button slot="append" icon="el-icon-search" @click="searchF()"></el-button>
        </el-input>   
      </div>
    </el-card>

    <el-menu
      :default-active="activeIndex2"
      class="el-menu-demo"
      mode="horizontal"
      @select="handleSelect"
      background-color="#fff"
      text-color="#000"
      content="center"
      active-text-color="#55aaff"
      padding-bottom="0px"
      >
      <el-menu-item index="1"><i class="el-icon-s-home"></i>首页</el-menu-item>
      <el-submenu index="2">
        <template slot="title"><i class="el-icon-menu"></i>分类</template>
        <el-menu-item index="2-1">猫咪</el-menu-item>
        <el-menu-item index="2-2">刺猬</el-menu-item>
        <el-submenu index="2-3">
          <template slot="title">鸟类</template>
          <el-menu-item index="2-4-1">全部</el-menu-item>
          <el-menu-item index="2-4-1">喜鹊</el-menu-item>
          <el-menu-item index="2-4-2">麻雀</el-menu-item>
          <el-menu-item index="2-4-3">鸳鸯</el-menu-item>
          <el-menu-item index="2-4-4">天鹅</el-menu-item>
          <el-menu-item index="2-4-5">其他</el-menu-item>
        </el-submenu>
        <el-menu-item index="2-4">鱼</el-menu-item>
        <el-menu-item index="2-5">其他</el-menu-item>
        </el-submenu>
      </el-submenu>
      <!--el-menu-item index="3"><i class="el-icon-document"></i>百科</el-menu-item-->
        <el-submenu index="3">
        <template slot="title"><i class="el-icon-menu"></i>百科</template>
        <el-menu-item index="3-1">猫咪</el-menu-item>
        <el-menu-item index="3-2">刺猬</el-menu-item>
        <el-submenu index="3-3">
          <template slot="title">鸟类</template>
          <el-menu-item index="3-4-1">喜鹊</el-menu-item>
          <el-menu-item index="3-4-2">麻雀</el-menu-item>
          <el-menu-item index="3-4-3">鸳鸯</el-menu-item>
          <el-menu-item index="3-4-4">天鹅</el-menu-item>
        </el-submenu>
        <el-menu-item index="3-4">鱼</el-menu-item>
        </el-submenu>
      </el-submenu>

      <el-menu-item index="4"><i class="el-icon-user"></i>我的</el-menu-item>
      <el-menu-item index="5"><i class="el-icon-circle-plus-outline"></i>发帖</el-menu-item>
    </el-menu>

  </div>

    <!--怎么才能居中？-->
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
    <el-button class="upload" @click="startupload()"> upload</el-button>


  <el-backtop>
  </el-backtop>

  </div>
</div>

</template>

<script>
export default {
  data() {
    
    return {
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
        {
          "postID":"456",
        "postDescrip":"asdadads",
        "images":[
          {
          "src":require('../../assets/Jhin.jpg'),
          }
        ]
        },
        {
          "postID":"789",
        "postDescrip":"asdadads",
        "images":[
          {
          "src":require('../../assets/bg1.jpg'),
          }
        ]
        },
        {
          "postID":"123",
        "postDescrip":"asdadads",
        "images":[
          {
          "src":require('../../assets/Jhin.jpg'),
          }
        ]
        }
      ],

    }
  },
  methods:{

      searchF()
      {
          //search for
        console.log(this.searchbar.input)
        
      },
      loadMore(){

      },
      getScroll(){

      },
      startupload(){
        this.$router.push('/postupload')
      },
      postDetail(Inp){
        this.$router.push({path:'/postDetail', query:{"postID":Inp} })
      },
      handleSelect(key, keyPath) {
        console.log(key);
        if(key=="5"){
          this.$router.push({path:'/postupload', query:{"userID":"this is userid","type":key} })
        }
        else if(key=="4"){
          this.$router.push({path:'/userinfo', query:{"userID":"this is userid","type":key} })
        }
        else if(key[0]=="3")
        {
          this.$router.push({path:'/baike', query:{"type":key} })
        }
      } 
  }
}
</script>

<style scoped>
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
/*白写了style wrng
.searchClass{
  border: 1px solid #c5c5c5;
  border-radius: 20px;
  background: #f4f4f4;
  margin-bottom:10px;
}
.searchClass .el-input-group__prepend {
  border: none;
  background-color: transparent;
  padding: 0 10px 0 30px;
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
}*/


// for content
  .line{
    padding :20px
  }
  .time {
    font-size: 13px;
    color: #999;
  }
  
  .bottom {
    margin-top: 13px;
    line-height: 12px;
  }

  .button {
    padding: 0;
    float: right;
  }
//for card

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

.userHeader{
  
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


  .clearfix:before,
  .clearfix:after {
      display: table;
      content: "";
  }
  
  .clearfix:after {
      clear: both
  }


</style>


