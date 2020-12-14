<template>
<div>
<!--header-->
<el-page-header @back="goBack" content="帖子详情">
</el-page-header>
<!--post detail-->
<div >
<el-card class = "Postcard"  :body-style="{ padding: '30px' }"  >
        <!--发帖人-->
    <div @click="getUserInfo()">
      <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" ></el-avatar>
      <span>this is username</span>
    </div>
        <div style="padding: 14px;" >
            <span class="PostDescription">{{postDetail.postDes}}</span>

            <!--imgs here-->
        <div class="SongList">
            <div class="covers" :style="{display:MinDisplay}">
            <div class="cover" v-for="(img,index) in postDetail.images" :key='index'>
            <el-image :src="img.src" width="90%" class="min" 
            :preview-src-list="getPreviewImgList(index)"></el-image>
            </div>
       </div>
       <!--div class="max" :style="{display:display}">
            <div @click="ZoomOut"  v-for="(img,index) in postDetail.images" :key='index' :class="[index===ShowIndex?'active':'None']" ><img :src="img.src" width="100%"></div>
        </div-->
    </div>
            <div class="bottom clearfix">
            <time class="time">time here</time>
            <!--el-button type="text" class="button">帖子详情</el-button-->
            </div>
            <el-button>点赞num</el-button>
        </div>
        <!--九宫格-->
            <div class="covers" > 
            </div>

</el-card>

</div>
<!--comment test here-->

 <div>
 <el-card>
         this is the comment card
        <div @click="inputFocus" class="my-reply">
            <el-avatar class="header-img" :size="40" :src="myHeader"></el-avatar>
            <div class="reply-info" >
                <div 
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
                <el-button class="reply-btn" size="medium" @click="sendComment" type="primary">发表评论</el-button>
            </div>
        </div>
        
        <div v-for="(item,i) in comments" :key="i" class="author-title reply-father">
            <el-avatar class="header-img" :size="40" :src="item.headImg"></el-avatar>
            <div class="author-info">
                <span class="author-name">{{item.name}}</span>
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
export default {
    //for comment

// const clickoutside = {
//     // 初始化指令
//     bind(el, binding, vnode) {
//     function documentHandler(e) {
//     // 这里判断点击的元素是否是本身，是本身，则返回
//         if (el.contains(e.target)) {
//             return false;
//         }
//     // 判断指令中是否绑定了函数
//         if (binding.expression) {
//             // 如果绑定了函数 则调用那个函数，此处binding.value就是handleClose方法
//             binding.value(e);
//         }
//     }
//     // 给当前元素绑定个私有变量，方便在unbind中可以解除事件监听
//     el.vueClickOutside = documentHandler;
//     document.addEventListener('click', documentHandler);
//     },
//     update() {},
//     unbind(el, binding) {
//     // 解除事件监听
//     document.removeEventListener('click', el.vueClickOutside);
//     delete el.vueClickOutside;
//   },
// };


  data() {
    name:'This is ArticleComment';
    return {
    ShowIndex:0,
    display: 'none',
    MinDisplay:'flex',
    imgSrcList:[],
    getpostID:this.$route.query.shopid,
    postDetail:{
        "postID":"this is id",
        "postDes":"this is description",
        "images":[
            {   "id":0,
                "src":require('../../assets/Jhin.jpg')},
            {   "id":1,
                "src":require('../../assets/bg2.jpg')},
            {   "id":2,
                "src":require('../../assets/Jhin.jpg')},
            {   "id":3,
                "src":require('../../assets/bg2.jpg')},
            {   "id":4,
                "src":require('../../assets/Jhin.jpg')},
            {   "id":5,
                "src":require('../../assets/bg2.jpg')},
        ],
        "comments":[
            
        ]
    },

    //for comment test
    btnShow: false,
    index:'0',
    replyComment:'',
    myName:'name1',
            myHeader:'https://ae01.alicdn.com/kf/Hd60a3f7c06fd47ae85624badd32ce54dv.jpg',
            myId:1,
            to:'',
            toId:-1,
            comments:[
                {
                    name:'name2',
                    id:2,
                    headImg:'https://ae01.alicdn.com/kf/Hd60a3f7c06fd47ae85624badd32ce54dv.jpg',
                    comment:'comment1',
                    time:'time here',
                    commentNum:2,
                    like:15,
                    inputShow:false,
                    reply:[
                        {
                            from:'test',
                            fromId:3,
                            fromHeadImg:'https://ae01.alicdn.com/kf/H94c78935ffa64e7e977544d19ecebf06L.jpg',
                            to:'name1',
                            toId:4,
                            comment:'comment2',
                            time:'timehere2',
                            commentNum:1,
                            like:15,
                            inputShow:false
                        },
                        {
                            from:'name3',
                            fromId:1123,
                            fromHeadImg:'https://ae01.alicdn.com/kf/Hf6c0b4a7428b4edf866a9fbab75568e6U.jpg',
                            to:'name1',
                            toId:19870621,
                            comment:'comment3',
                            time:'timehere3',
                            commentNum:0,
                            like:5,
                            inputShow:false
 
                        }
                    ]
                },
            ]
        }
    },
  methods:{
      goBack(){
        this.$router.push({path:'/mainposts', query:{} })
      },
        getPreviewImgList(index){
            let arr = []
            let i = 0;
            for(i;i < this.postDetail.images.length;i++){
                arr.push(this.postDetail.images[i+index].src);
                if(i+index >= this.postDetail.images.length-1){
                index = 0-(i+1);
                }
            }
            console.log(arr);
        return arr;
        },
    getUserInfo()
    {
        this.$router.push({path:'/userinfo', query:{} })//tmp user id
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
        sendComment(){
            if(!this.replyComment){
                 this.$message({
                    showClose: true,
                    type:'warning',
                    message:'评论不能为空'
                })
            }else{
                let a ={}
                let input =  document.getElementById('replyInput')
                let timeNow = new Date().getTime();
                let time= this.dateStr(timeNow);
                a.name= this.myName
                a.comment =this.replyComment
                a.headImg = this.myHeader
                a.time = time
                a.commentNum = 0
                a.like = 0
                this.comments.push(a)
                this.replyComment = ''
                input.innerHTML = '';
 
            }
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
  }
}
</script>

<style acoped>
  .SongList{
        width: 40%;
    }
    .covers{
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
    }
    .cover{
        display: flex;
        justify-content: center;
        width: 33%;
        margin: 10px 0;
    }
    .min{
        border-radius: 10px;
        cursor: zoom-in;
    }
    .max{
        cursor: zoom-out;
        width: 100%;

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