<template>
  <div>
    <div>
      <!--header-->
      <el-page-header @back="goBack" content="帖子详情">
      </el-page-header>
      <!--post detail-->
    </div>

    <el-card class="Postcard" :body-style="{padding: '30px'}">
      <div @click="getUserInfo()">
        <el-avatar :src="avatar_dict[postDetail.user_name]"></el-avatar>
        <span>{{postDetail.user_name}}</span>
      </div>

      <div style="padding: 14px;">
        <span class="PostDescription">{{postDetail.description}}</span>
        <div class="SongList">
          <div class="covers" :style="{display:MinDisplay}">
            <div class="cover" v-for="(img,index) in postDetail.images" :key='index'>
              <el-image :src="img" width="90%" class="min" :lazy="true" :preview-src-list="getPreviewImgList(index)">
              </el-image>
            </div>
          </div>
        </div>
      </div>
        <div>
          <el-button class="location-btn" @click="showLocation()">位置<i class="el-icon-location"></i></el-button>
        </div>
      <div class="bottom clearfix">
        <p class="pid">#{{postDetail.pid}}</p>
        <time class="time">{{postDetail.time}}</time>     
      </div>

      
    </el-card>

    <!--comment test here-->

    <el-card>
    <!--comment Box-->
      <div class="my-reply">
        <el-avatar class="header-img" :size="40" :src="avatar_dict[myName]"></el-avatar>
        <div class="reply-info">
          <el-input placeholder="输入评论..." v-model="replyComment" autocomplete="off" class="reply-input"></el-input>
        </div>
        <div class="reply-btn-box" v-show="btnShow">
          <el-button class="reply-btn" size="medium" @click="send_comment()" type="primary">发表评论</el-button>
        </div>
      </div>
    <!--comments-->
      <div v-for="(item,i) in comments" :key="i" class="author-title">
        <el-card>
          <div class="comment-header" @click="showUserDetail(item.user_name)">
          <el-avatar class="header-img" :size="40" :src="avatar_dict[item.user_name]"></el-avatar>
          <span class="name">{{item.user_name}}</span>
          </div>

          <div class="talk-box">
            <p>
              <span class="reply">{{item.comment}}</span>
            </p>
          </div>
          <span class="time">{{item.time}}</span>
        </el-card>
      </div>
    </el-card>
  </div>
</template>

<script>
  import Qs from 'qs'
  import axios from "axios"

  export default {



    data() {
      return {
        ShowIndex: 0,
        display: 'none',
        MinDisplay: 'flex',
        imgSrcList: [],
        postDetail: {},

        avatar_dict:new Array(),
        default_avater:'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
        btnShow: true,
        index: '0',
        replyComment: '',
        myName: localStorage.getItem('tmp_username'),

        to: '',
        toId: -1,
        comments: []
      }
    },
    methods: {
      get_post(pid) {
        var datas = {
          'type': 'view_posts',
          'start_index': pid,
          'post_num': 1
        };
        var params = Qs.stringify(datas);
        console.log(datas, params);
        axios({
            url: 'index',
            method: 'post',
            data: params
          }).then((res) => {
            if (res.data.succ) {
              console.log('succ', res.data);
              this.set_postDetail(res.data.post_info_list[0]);
              this.get_replies(this.$route.query.pid);//执行完毕之后回调
            } else {
              console.log("res_error", res);
            }
          })
          .catch((err) => {
            console.log("catch_error", err);
          });
      },

      get_replies(pid) {
        var datas = {
          'type': 'view_replies',
          'pid': pid
        };
        var params = Qs.stringify(datas);
        console.log(datas, params);
        axios({
            url: 'index',
            method: 'post',
            data: params
          }, ).then((res) => {
            if (res.data.succ) {
              console.log('succ', res.data);
              this.set_replyDetail(res.data.reply_info_list);
              this.get_avatars();
            } else {
              console.log("res_error", res);
            }
          })
          .catch((err) => {
            console.log("catch_error", err);
          });
      },

      send_comment() {
        if (!this.replyComment) {
          this.$message({
            showClose: true,
            type: 'warning',
            message: '评论不能为空'
          })
        } else {
          var datas = {
            'type': 'comment_post',
            'jwt': localStorage.getItem('token'),
            'reply': {
              'post': this.$route.query.pid,
              'description': this.replyComment
            }
          };
          // var params = datas;
          var params = Qs.stringify(datas);
          console.log(datas, params);
          axios({
              url: 'index',
              method: 'post',
              data: params
            }, ).then((res) => {
              if (res.data.succ) {
                console.log('succ', res.data);
                this.get_replies(this.$route.query.pid);
                //清空输入框
                this.replyComment="";
              } else {
                console.log("res_error", res);
              }
            })
            .catch((err) => {
              console.log("catch_error", err);
            });
        }
      },

      set_postDetail(post) {
        this.postDetail.pid = post.pid;
        this.postDetail.description = post.description;
        this.postDetail.position = post.position;
        this.postDetail.images = [];
        let image_list = [];
        if (post.image_src) this.postDetail.images = post.image_src.split(',');

        this.postDetail.time = new Date(post.timestamp * 1000);
        // 必须用$set才能提醒视图更新内容，不然视图是检测不到data中对象的某个属性发生更新的
        this.$set(this.postDetail, 'user_name', post.user_name);
        console.log("postDetail: ", this.postDetail);
      },

      set_replyDetail(replies) {
        console.log(replies);
        this.comments=[];
        for (var reply of replies) {
          var images_list = '';
          if (reply.image_src) image_list = reply.image_src.split(',');
          this.comments.push({
            user_name: reply.user_name,
            user_img: reply.user_img,
            comment: reply.description,
            time: new Date(reply.timestamp * 1000),
            images: images_list
          })
        }
        console.log(this.comments);
      },

      get_avatars()//axios请求所有的头像
      {
        this.avatar_dict={};
        var name_list=[];
        var that = this;
        name_list.push(this.postDetail.user_name);
        console.log("post owner username",that.postDetail.user_name);
        console.log(that.postDetail);
        if(!name_list.includes(this.myName))
        {
          name_list.push(this.myName);
        } 
        for(let comment of this.comments){
          if(!name_list.includes(comment.user_name)){
            name_list.push(comment.user_name);
          }
        }
        console.log(name_list);
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
      showUserDetail(name){
        this.$router.push({
            path: '/userinfo',
            query: {
              "username": name,
              // "type": key
            }
        })
      },
      goBack() {
        this.$router.go(-1);
      },
      //for preview
      getPreviewImgList(index) {
        let arr = []
        let i = 0;
        for (i; i < this.postDetail.images.length; i++) {
          arr.push(this.postDetail.images[i + index]);
          if (i + index >= this.postDetail.images.length - 1) {
            index = 0 - (i + 1);
          }
        }
        console.log(arr);
        return arr;
      },

      getUserInfo() {
        this.$router.push({
          path: '/userinfo',
          query: {
            "username": this.postDetail.user_name
          }
        }) //tmp user id
      },


      showLocation()
      {
        var _this = this;
        if(this.postDetail.position){
          console.log(this.postDetail.position)
          this.$router.push({
            path: '/showLocation',
            query: {
              "position":this.postDetail.position
            }
          })
        }
    }
    },

    mounted: function () {
      console.log('created pid: ', this.$route.query.pid);
      this.get_post(this.$route.query.pid);

      // this.get_avatars();
    },


  }

</script>

<style scoped>
  .SongList {
    width: 60%;
    display: table-cell;
  }
  .Postcard{
    
    margin-bottom:20px;
  }
  .covers {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    // width:700px;
  }

  .cover {
    display: flex;
    justify-content: center;
    width: 33%;
    // height:33%;
    // width:200px;
    height: 300px;
    margin: 5px 0px;
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
  .my-reply {
    padding: 10px;
    background-color: #fafbfc
  }

  .header-img {
    display: inline-block;
    vertical-align: top;
  }
  .comment-header{
    float:left;
    margin-top:10px;
    display:block;
  }
  .reply-info {
    display: inline-block;
    margin-left: 5px;
    width: 90%;

  }

  .reply-btn-box {
    height: 25px;
    margin: 10px 0;
  }
  .location-btn{
    margin-bottom:10px;
  }
  .reply-btn {
    position: relative;
    margin-right: 15px
  }
  .name{
    padding:10px 10px;
    font-size: 20px;
  }
  .author-title {
    padding: 10px;
  }
  .reply-input
  {
    style.padding:8px 8px;
    border:2px,solid blue;
  }
</style>
