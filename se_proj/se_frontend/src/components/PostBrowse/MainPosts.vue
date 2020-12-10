<template>
<div>
     <div class="allbox">
    <div>
      <el-input placeholder="请输入搜索内容" v-model="searchbar.input" autocomplete="off" class="searchClass">
        <el-button slot="append" icon="el-icon-search" @click="searchF('currentDate')"></el-button>
      </el-input>
    </div>

    <!--怎么才能居中？-->
    <div class="CardList">
    <el-row >
      <div  v-for="(post,index) in posts" :key='post' @click="postDetail(post.postID)">
        <el-card class = "Showcard"  :body-style="{ padding: '30px' }"  >
        <div style="padding: 14px;" >
            <span class="PostDescription">{{post.postDescrip}}</span>
            <div class="bottom clearfix">
            <time class="time">{{ currentDate }}</time>
            <!--el-button type="text" class="button">帖子详情</el-button-->
            </div>
        </div>
        <!--选择每个帖子预先显示一张图，详情之后再显示其他图-->

            <div class="covers" >
                <!--img :src="img.src" width="90%" class="min" alt=""-->
                <img class="image" :src="post.images[0].src"/>
            </div>

        </el-card>
      </div>
    <!--/el-col-->
    </el-row>
    </div>
    <el-button class="upload" @click="startupload()"> upload</el-button>


  <el-backtop >
  </el-backtop>

  </div>
</div>

</template>

<script>
export default {
  data() {
    
    return {
      currentDate:new Date(),
      searchbar:{
      input: '',
      select: '',
      
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
      searchF(Inp)
      {
          //search for
          console.log(Inp)
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
      }
  }
}
</script>

<style acoped>
.allbox{
  background: url("../../assets/bg2.jpg");
  background-size: cover;
  background-position: center center;
  background-repeat: no-repeat;
  background-attachment: fixed;
  width: 100%;
  height: 100%;

}

.searchClass{
  // position:fixed;
  border: 1px solid #c5c5c5;
  border-radius: 20px;
  background: #f4f4f4;
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
  position:center center;
}
.Showcard{
  width: 70%;
  height: 70%;
  margin-top: 13px;
  position:center;  
}
.image {
    height: 500px;
    width: auto;
    position: center;
    margin: 0 auto;
    display: block;
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


