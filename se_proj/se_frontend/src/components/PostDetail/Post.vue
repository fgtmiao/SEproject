<template>
<div>

<div>
<!--header-->
<el-page-header @back="goBack" content="帖子详情">
</el-page-header>
<!--post detail-->
</div>

<el-card class = "Postcard"  :body-style="{ padding: '30px' }"  >
    <div @click="getUserInfo()">
      <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" ></el-avatar>
      <span>{{postDetail.user_name}}</span>
    </div>

    <div style="padding: 14px;" >
      <span class="PostDescription">{{postDetail.description}}</span>
      <div class="SongList">
        <div class="covers" :style="{display:MinDisplay}">
        <div class="cover" v-for="(img,index) in postDetail.images" :key='index'>
        <el-image :src="img" width="90%" class="min" :lazy="true"
          :preview-src-list="getPreviewImgList(index)"></el-image>
        </div> 
        <!--div v-for="image in postDetail.images" :key="image.value" class="imgbox"><img class="image" v-bind:src="image"></div-->
        </div>
      </div>
    </div>

    <div class="bottom clearfix">
      <p class="pid">#{{postDetail.pid}}</p>
      <time class="time">{{postDetail.time}}</time>
      <!--el-button type="text" class="button">帖子详情</el-button-->
    <el-button>点赞num</el-button>
    </div>
</el-card>

<!--comment test here-->

<el-card>
         this is the comment card
        <div @click="inputFocus" class="my-reply">
            <el-avatar class="header-img" :size="40" :src="myHeader"></el-avatar>
            <div class="reply-info" >
                <div 
                v-model="replyComment"
                tabindex="0" 
                contenteditable="true" 
                id="replyInput" 
                spellcheck="false" 
                placeholder="输入评论..." 
                class="reply-input" 
                @focus="showReplyBtn"  
                @input="onDivInput($event)"
                >
                </div>
            </div>
            <div class="reply-btn-box" v-show="btnShow">
                <el-button class="reply-btn" size="medium" @click="send_comment" type="primary">发表评论</el-button>
            </div>
        </div>
        
        <div v-for="(item,i) in comments" :key="i" class="author-title reply-father">
            <el-avatar class="header-img" :size="40" :src="item.headImg"></el-avatar>
            <div class="author-info">
                <span class="author-name">{{item.user_name}}</span>
                <span class="author-time">{{item.time}}</span>
            </div>
            <div class="icon-btn">
                <span @click="showReplyInput(i,item.name,item.id)"><i class="iconfont el-icon-s-comment"></i>{{item.commentNum}}</span>
                <i class="iconfont el-icon-caret-top"></i>{{item.like}}
            </div>
            <div class="talk-box">
                <p>
                    <span class="reply">{{item.comment}}</span>
                </p>
            </div>
            <div class="reply-box">
                <div v-for="(reply,j) in item.reply" :key="j" class="author-title">
                    <el-avatar class="header-img" :size="40" :src="reply.fromHeadImg"></el-avatar>
                    <div class="author-info">
                        <span class="author-name">{{reply.from}}</span>
                        <span class="author-time">{{reply.time}}</span>
                    </div>
                    <div class="icon-btn">
                        <span @click="showReplyInput(i,reply.from,reply.id)"><i class="iconfont el-icon-s-comment"></i>{{reply.commentNum}}</span>
                        <i class="iconfont el-icon-caret-top"></i>{{reply.like}}
                    </div>
                    <div class="talk-box">
                        <p>
                            <span>回复 {{reply.to}}:</span>
                            <span class="reply">{{reply.comment}}</span>
                        </p>
                    </div>
                    <div class="reply-box">
 
                    </div>
                </div>
            </div>
            <div  v-show="_inputShow(i)" class="my-reply my-comment-reply">
                <el-avatar class="header-img" :size="40" :src="myHeader"></el-avatar>
                <div class="reply-info" >
                    <div tabindex="0" contenteditable="true" spellcheck="false" placeholder="输入评论..."   @input="onDivInput($event)"  class="reply-input reply-comment-input"></div>
                </div>
                <div class=" reply-btn-box">
                    <el-button class="reply-btn" size="medium" @click="sendCommentReply(i,j)" type="primary">发表评论</el-button>
            </div>
        </div>
    
        </div>
</el-card>



</div>
</div>
</template>

<script>

import Qs from 'qs'
import axios from "axios"

export default {



  data() {
    return {
      ShowIndex:0,
      display: 'none',
      MinDisplay:'flex',
      imgSrcList:[],
      postDetail:{
      },

      //for comment test
      btnShow: false,
      index:'0',
      replyComment:'',
      myName:'name1',
      myHeader:'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
      myId:1,
      to:'',
      toId:-1,
      comments:[
      ]
    }
  },
  methods:{
    get_post(pid) {
      var datas = {'type': 'view_posts', 'start_index': pid, 'post_num': 1};
      var params = Qs.stringify(datas);
      console.log(datas, params);
      axios({url: 'index', method: 'post', data: params}).then((res) => {
          if (res.data.succ) {
            console.log('succ', res.data);
            this.set_postDetail(res.data.post_info_list[0]);
          }
          else {
            console.log("res_error", res);
          }
        })
        .catch((err) => {
          console.log("catch_error", err);
        });
    },

    get_replies(pid) {
      var datas = {'type': 'view_replies', 'pid': pid};
      var params = Qs.stringify(datas);
      console.log(datas, params);
      axios({url: 'index', method: 'post', data: params}, ).then((res) => {
          if (res.data.succ) {
            console.log('succ', res.data);
            this.set_replyDetail(res.data.reply_info_list);
          }
          else {
            console.log("res_error", res);
          }
        })
        .catch((err) => {
          console.log("catch_error", err);
        });
    },

    send_comment(){
        if (!this.replyComment) {
          this.$message({
            showClose: true,
            type:'warning',
            message:'评论不能为空'
          })
        } else {
          var datas = {
            'type': 'comment_post', 'jwt': localStorage.getItem('token'),
            'reply': {'post': this.$route.query.pid, 'description': this.replyComment} 
          };
          // var params = datas;
          var params = Qs.stringify(datas);
          console.log(datas, params);
          axios({url: 'index', method: 'post', data: params}, ).then((res) => {
              if (res.data.succ) {
                console.log('succ', res.data);
                this.get_replies(this.$route.query.pid);
              }
              else {
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
      this.postDetail.images = [];
      let image_list = [];
      if (post.image_src) this.postDetail.images = post.image_src.split(',');
      //是要加个require吧
      // console.log(post.image_src)
    
      // if (post.image_src) {
      //   image_list = post.image_src.split(',');
        
      //   };
      // console.log("imagelist",image_list);  
      
      
      // for(let i=0;i < image_list.length;i++)
      // {
      //   let dic = {"src":require(image_list[i])};
      //   console.log("dic",dic)
      //   this.postDetail.images.push(dic);
      // }
      this.postDetail.time = new Date(post.timestamp * 1000);
      // 必须用$set才能提醒视图更新内容，不然视图是检测不到data中对象的某个属性发生更新的
      this.$set(this.postDetail, 'user_name', post.user_name);
      console.log("postDetail: ", this.postDetail);
    },

    set_replyDetail(replies) {
      console.log(replies);
      for (var reply of replies) {
        var images_list = '';
        if (reply.image_src) image_list = reply.image_src.split(',');
        this.comments.push({
          user_name: reply.user_name, user_img: reply.user_img, comment: reply.description,
          time: new Date(reply.timestamp * 1000), images: images_list
        })
      }
      console.log(this.comments);
    },


    goBack(){
      this.$router.push({path:'/mainposts', query:{} })
    },

    getPreviewImgList(index){
        let arr = []
        let i = 0;
        for(i;i < this.postDetail.images.length;i++){
            arr.push(this.postDetail.images[i+index]);
            if(i+index >= this.postDetail.images.length-1){
            index = 0-(i+1);
            }
        }
        console.log(arr);
    return arr;
    },

    getUserInfo()
    {
        this.$router.push({path:'/userinfo', query:{"username":this.postDetail.user_name} })//tmp user id
    },

    inputFocus(){
        var replyInput = document.getElementById('replyInput');
        replyInput.style.padding= "8px 8px"
        replyInput.style.border ="2px solid blue"
        replyInput.focus()
    },

    showReplyBtn(){
        this.btnShow = true
    },

    hideReplyBtn(){
        this.btnShow = false
        replyInput.style.padding= "10px"
        replyInput.style.border ="none"
    },

    showReplyInput(i,name,id){
        this.comments[this.index].inputShow = false
        this.index =i
        this.comments[i].inputShow = true
        this.to = name
        this.toId = id
    },

    _inputShow(i){
        return this.comments[i].inputShow 
    },

    sendCommentReply(i,j){
        if(!this.replyComment){
            this.$message({
                showClose: true,
                type:'warning',
                message:'评论不能为空'
            })
        }else{
            let a ={}
            let timeNow = new Date().getTime();
            let time= this.dateStr(timeNow);
            a.from= this.myName
            a.to = this.to
            a.fromHeadImg = this.myHeader
            a.comment =this.replyComment
            a.time = time
            a.commentNum = 0
            a.like = 0
            this.comments[i].reply.push(a)
            this.replyComment = ''
            document.getElementsByClassName("reply-comment-input")[i].innerHTML = ""
        }
    },

    onDivInput: function(e) {
        this.replyComment = e.target.innerHTML;
    },

    dateStr(date){
        //获取js 时间戳
        var time=new Date().getTime();
        //去掉 js 时间戳后三位，与php 时间戳保持一致
        time=parseInt((time-date)/1000);
        //存储转换值 
        var s;
        if(time<60*10){//十分钟内
            return '刚刚';
        }else if((time<60*60)&&(time>=60*10)){
            //超过十分钟少于1小时
            s = Math.floor(time/60);
            return  s+"分钟前";
        }else if((time<60*60*24)&&(time>=60*60)){ 
            //超过1小时少于24小时
            s = Math.floor(time/60/60);
            return  s+"小时前";
        }else if((time<60*60*24*30)&&(time>=60*60*24)){ 
            //超过1天少于30天内
            s = Math.floor(time/60/60/24);
            return s+"天前";
        }else{ 
            //超过30天ddd
            var date= new Date(parseInt(date));
            return date.getFullYear()+"/"+(date.getMonth()+1)+"/"+date.getDate();
        }
    }
  },

  created: function() {
    console.log('created pid: ', this.$route.query.pid);
    this.get_post(this.$route.query.pid);
    this.get_replies(this.$route.query.pid);
  }
}
</script>

<style scoped>
.SongList{
    width: 60%;
    display:table-cell;
}
.covers{
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        // width:700px;
}
.cover{
        display: flex;
        justify-content: center;
        width: 33%;
        // height:33%;
        // width:200px;
        height:300px;
        margin: 5px 0px;
}
.min{
        border-radius: 10px;
        cursor: zoom-in;
}
.max{
        cursor: zoom-out;
        width: 100%;
    }

  .pid {
    font-size: 13px;
    color: #999;
    position: absolute;
    left: 10px; bottom: 5px; margin: 0px;
  }

.time {
    font-size: 13px;
    color: #999;
  }
//for cpmment

.my-reply{
    padding:10px;
    background-color:#fafbfc
    }
    .header-img{
        display:inline-block;
        vertical-align:top;
    }
    .reply-info{
        display:inline-block;
        margin-left:5px;
        width:90%;

    }
.reply-btn-box
       { height:25px;
        margin:10px 0;}
.reply-btn
{            position:relative;
            margin-right:15px}

.author-title
{    padding:10px;
    .header-img
        {display:inline-block;
        vertical-align:top;}
}
    .icon-btn
{        width:30%;
        padding:0 !important; 
        float:right;}


    .reply-box
        {margin:10px 0 0 50px;
        background-color:#efefef}

</style>