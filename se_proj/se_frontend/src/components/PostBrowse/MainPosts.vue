<template>
  <div>
    <!--header父子组件太容易出bug，还是老老实实复制粘贴
首页分类搜索结果都在这个界面做-->

    <div class="allbox">
      <div class="mainheader">
        <el-card class="headercard">
          <el-divider><span class="headertext">PASS小动物照片分享平台</span></el-divider>
          <div>
            <el-input placeholder="请输入搜索帖子内容" v-model="searchbar.input" autocomplete="off" class="searchClass">
              <el-button slot="append" icon="el-icon-search" @click="searchF()"></el-button>
            </el-input>
          </div>
        </el-card>

        <el-menu :default-active="activeIndex2" class="el-menu-demo" mode="horizontal" @select="handleSelect"
          background-color="#fff" text-color="#000" content="center" active-text-color="#55aaff" padding-bottom="0px">
          <el-menu-item index="1"><i class="el-icon-s-home"></i>首页</el-menu-item>
          <el-submenu index="2">
            <template slot="title"><i class="el-icon-menu"></i>分类</template>
            <el-menu-item index="2-1">猫咪</el-menu-item>
            <el-menu-item index="2-2">刺猬</el-menu-item>
            <el-submenu index="2-3">
              <template slot="title">鸟类</template>
              <el-menu-item index="2-3-1">喜鹊</el-menu-item>
              <el-menu-item index="2-3-2">麻雀</el-menu-item>
              <el-menu-item index="2-3-3">鸳鸯</el-menu-item>
              <el-menu-item index="2-3-4">天鹅</el-menu-item>
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

      <!--希望在cardlist中实现无限滚动，范围限制成功，但是一直触发load？-->
      <div class="CardList" v-infinite-scroll="loadMore" infinite-scroll-disabled="busy" >
        <el-row class="cardrow" >
          <div v-for="(post,index) in posts" :key='post.index'>
            <el-card class="Showcard" :body-style="{ padding:'0px' }">
              <div @click="postDetail(post.pid)">
                <div style="padding: 14px;">
                  <div class="userHeader">
                    <el-avatar :src="avatar_dict[post.user_name]"></el-avatar>
                    <span>{{post.user_name}}</span>
                  </div>
                  <span class="PostDescription">{{post.description}}</span>
                  <div class="bottom clearfix">
                    <!--el-button type="text" class="button">帖子详情</el-button-->
                  </div>
                </div>
                <!--选择每个帖子预先显示一张图，详情之后再显示其他图-->
                <div class="covers">
                  <!--img :src="img.src" width="90%" class="min" alt=""-->
                  <li class="imgbox"><img class="image" :src="post.images[0]" /></li>
                </div>
                <div>
                <p class="pid">#{{post.pid}}</p>
                <time class="time">{{ post.time }}</time>
                </div>
                <!--i class="el-icon-location-information"></i>
                <i class="el-icon-picture-outline"></i-->
              </div>
            </el-card>
          </div>
        </el-row>
      </div>
      <!--el-button class="upload" @click="startupload()"> upload</el-button-->

      <el-backtop>
      </el-backtop>
      <span v-if="nomore">没有更多了</span>
    </div>
  </div>

</template>

<script>
  import Qs from 'qs'
  import axios from "axios"

  export default {
    data() {

      return {
        default_avater:"https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png",
        busy:false,
        nomore:false,//数据库是否还有数据
        activeIndex2: '1',
        typeSelect:'1',//选择的类别
        searchbar: {
          input: '',
        },
        last_viewed_index: -1, // 默认值为-1，表示还没有开始浏览帖子
        posts: [
        ],
        //维护一个avatar字典,"username":url
        avatar_dict:new Array(),
        map_dict:{
        "2-1":"猫咪",
        "2-2":"刺猬",
            // <el-submenu index="3-3">
              // <template slot="title">鸟类</template>
        "2-3-1":"喜鹊",
        "2-3-2":"麻雀",
        "2-3-3":"鸳鸯",
        "2-3-4":"天鹅",
        "2-4":"鱼",
        "2-5":"其他",
        }
      }
    },
    methods: {
      get_posts(start_index, animal_class, position) {
        var datas = {
          'type': 'view_posts'
        };
        if (start_index > 0) datas['start_index'] = start_index;
        if (animal_class) datas['animal_class'] = animal_class;
        if (position) datas['position'] = position;
        datas['post_num']=10;
        var params = Qs.stringify(datas);
        console.log(datas, params);
        axios({
            url: 'index',
            method: 'post',
            data: params
          }, )
          .then((res) => {
            if (res.data.succ) {
              //在此处判定是否还有帖子存在
              if(res.data.post_info_list.length==0)
              {
                this.busy=true;
                this.nomore = true;
              }
              else{
                this.add_posts(res.data.post_info_list);
              }
            } else {
              console.log("res_error", res);
            }
          })
          .catch((err) => {
            console.log("catch_error", err);
          });
      },

      searchF() {
        //跳转到搜索界面吧
        // console.log(this.searchbar.input)
        if(this.searchbar.input.length==0){
          this.$message({
            showClose: true,
            type: 'warning',
            message: '搜索内容不能为空'
          });
        }
        else{
        this.$router.push({
          path: '/searchRes',
          query: {
            "search": this.searchbar.input
          }
        })
        }
      },
      loadMore(){
        
        this.busy=true;//此期间不再触发
        console.log("loading")//为什么会一直触发？
        console.log("type",this.typeSelect)
        console.log("search",this.searchbar.input)//搜索时typeSelect换到另一个界面？
        if(this.typeSelect==1)
        {
          if(this.posts.length==0){
            this.get_posts();
            this.busy=false;
          }
          else{
            var request_pid=this.posts[this.posts.length-1].pid-1;
            console.log(request_pid);
            if(request_pid==0)//我开始理解树洞的循环显示了，可以整一个申请之后不再set用作分类
            {
              this.busy=true;
              this.nomore=true;
            }
            else{
            this.get_posts(request_pid);
            this.busy=false;
            }
          }
        }
        else if(this.typeSelect[0]==2){
          //根据类别返回
          if(this.posts.length==0){
            this.get_posts(0,this.map_dict[this.typeSelect],);
            this.busy=false;
          }
          else{
            var request_pid=this.posts[this.posts.length-1].pid-1;
            console.log(request_pid);
            if(request_pid==0)//理解了树洞的循环显示
            {
              this.busy=true;
              this.nomore=true;
            }
            else{//如果无了咋办啊
            this.get_posts(request_pid,this.map_dict[this.typeSelect],);
            this.busy=false;
            }
          }
        }
      },

      startupload() {
        this.$router.push('/postupload')
      },
      postDetail(pid) {
        this.$router.push({
          path: '/postDetail',
          query: {
            "pid": pid
          }
        })
      },
      handleSelect(key, keyPath) {
        console.log(key);
        if (key == "5") {
          this.$router.push({
            path: '/postupload',
            query: {
              "username": "this is userid",
              "type": key
            }
          })
        } else if (key == "4") {
          this.$router.push({
            path: '/userinfo',
            query: {
              "username": localStorage.getItem('tmp_username'),
              // "type": key
            }
          })
        } else if (key[0] == "3") {
          this.$router.push({
            path: '/baike',
            query: {
              "type": key
            }
          })
        }
        else if(key[0]==2){//数组清零，type更换

          this.busy=false;//清空状态
          this.nomore=false;
          this.posts.splice(0,this.posts.length,);
          this.typeSelect=key;
          console.log(this.posts);
          this.loadMore();
        }
        else if(key[0]==1){//数组清零，type更换

          this.busy = false;
          this.nomore=false;
          this.posts.splice(0,this.posts.length,);
          this.typeSelect=key;
          console.log(this.posts);
          this.loadMore();
        }
      },
      add_posts(posts_list) {
        // console.log(posts_list);
        for (var post of posts_list) {
          var images_list = '';
          if (post.image_src) images_list = post.image_src.split(',');
          this.posts.push({
            user_name: post.user_name,
            description: post.description,
            time: new Date(post.timestamp * 1000),
            images: images_list,
            pid: post.pid
          })
        }
        console.log("this.posts push over");
        let that = this;
        console.log("before process avatar",this.avatar_dict)//已经有了
        //还是优化一下吧，用namelist
        var name_list=[];
        for(let post of that.posts){
          if(!name_list.includes(post.user_name)){
            name_list.push(post.user_name);
          }
        }
        console.log("user name list",name_list);
        for(let name of name_list)
        {
          //如果刷新出的是没有头像缓存的用户
          // console.log(post.user_name,that.avatar_dict)
          if(!that.avatar_dict.hasOwnProperty(name))
          {
            console.log(name,"not in dict")
            var datas = {
              'type': 'get_user_info'
            };
            //用户头像信息
            datas['user_name']=name;
            var params = Qs.stringify(datas);
            axios({
                url: 'userinfo',
                method: 'post',
                data: params
              }).then((res)=>{
                console.log(res);
                if(res.data.user_info.user_fig){
                  // console.log("set",post.user_name,res.data.user_info.user_fig)
                  that.$set(that.avatar_dict,name,res.data.user_info.user_fig);
                }
                else{
                that.$set(that.avatar_dict,name,that.default_avater);  
                }
              }).catch((err)=>{
                console.log("err",err);
                that.$set(that.avatar_dict,name,that.default_avater);
              })
          }
        }
      }
    },
    created: function () {
      console.log("created!");
    },
  }

</script>

<style scoped>
  .headercard {
    padding-top: 30px;
    border-radius: 0px;
  }

  .headertext {
    color: #101010;
    font-size: 30px;
  }

  .allbox {
    background-image: url("../../assets/bg_new.jpg");
    background-size: contain;
    height: 100%;
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
  .line {
    padding: 20px
  }

  .pid {
    font-size: 13px;
    color: #999;
    position: absolute;
    left: 10px;
    // bottom: 5px;
    margin: 0px;
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


  .CardList {
    height:700px;
    overflow-y:auto;
  }

  .Showcard {
    width: 60%;
    height: 70%;
    margin-top: 13px;
  }

  .userHeader {}

  .imgbox {
    font-size: 0;
    vertical-align: middle;
    justify-content: center;
    position: center center;
    display: inline-block;
    width: 500px;
    height: 300px;
    line-height: 240px;
    text-align: center;
    // outline: 1px solid #000;
    margin-bottom: 10px
  }

  .imgbox img {
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
