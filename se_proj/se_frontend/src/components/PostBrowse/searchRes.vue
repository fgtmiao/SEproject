<template>
<div>
    <el-page-header @back="goBack" content="返回主页">
    </el-page-header>

      <!--div class="CardList" v-infinite-scroll="loadMore" infinite-scroll-disabled="busy" -->
      <div class="CardList">
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
                  </div>
                </div>
                <div class="covers">
                  <li class="imgbox"><img class="image" :src="post.images[0]" /></li>
                </div>
                <p class="pid">#{{post.pid}}</p>
                <time class="time">{{ post.time }}</time>
                <!--i class="el-icon-location-information"></i>
                <i class="el-icon-picture-outline"></i-->
              </div>
            </el-card>
          </div>
        </el-row>
      <span>没有其他结果了</span>
      </div>

    </div>
</template>


<script>
import Qs from 'qs'
import axios from "axios"
export default {
    //依然需要头像系统
    data(){
        return{
        posts: [
        ],
        searching:this.$route.query.search,//搜索内容
        avatar_dict:new Array(),
        default_avater:"https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png",
        }
    },
    methods:{
      
    goBack() {
        this.$router.go(-1);
      },
    add_posts(posts_list) {
        console.log(posts_list);
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
        console.log(this.posts)
                let that = this;
        console.log("before process avatar",this.avatar_dict)//已经有了
        //还是优化一下吧，用namelist
        var name_list=[];
        for(let post of that.posts){
          if(!name_list.includes(post.user_name)){
            name_list.push(post.user_name);
          }
        }
        // console.log("user name list",name_list);
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
      },
      searchF(inp){
          //请求posts
        var datas = {
          'type': 'view_posts'
        };

        datas['description'] = inp;
        // datas['post_num']=10;
        var params = Qs.stringify(datas);
          axios({
            url: 'index',
            method: 'post',
            data: params
          }).then((res)=>{
              this.add_posts(res.data.post_info_list);
          }).catch((err)=>{
            console.log(err);
          })
      },
      postDetail(pid) {
        this.$router.push({
          path: '/postDetail',
          query: {
            "pid": pid
          }
        })
      },
    },
    mounted:function(){

        console.log("this is",this.searching)
        this.searchF(this.searching)
    }
    }
</script>

<style scoped>
  .allbox {
    background-image: url("../../assets/bg_new.jpg");
    background-size: contain;
    height: 100%;
    background-position: 400px 0px;
    background-repeat: no-repeat;
    background-attachment: fixed;
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
    .CardList {
    height:900px;
    overflow-y:auto;
  }

  .Showcard {
    width: 60%;
    height: 70%;
    margin-top: 13px;
  }
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

</style>
