<template>
  <div>
    <!--header here-->
    <div class="allbox">

      <el-page-header @back="goBack" content="个人主页">
      </el-page-header>
      <div class="userInfoCard">
        <el-card>
          <el-avatar :src="default_avater"></el-avatar>
          <span>{{tmp_username}}</span>

          <el-button v-if='ismine' @click="dialogVisible=true">修改头像</el-button>
        </el-card>
      </div>

      <!--他的帖子-->
      <span v-if='ismine'>我的帖子</span>
      <span v-else>TA的帖子</span>
      <div class="CardList" infinite-scroll-disabled="busy">
        <el-row class="cardrow">
          <div v-for="(post,index) in posts" :key='post.index'>
            <el-card class="Showcard" :body-style="{ padding:'0px' }">
              <div @click="postDetail(post.pid)">
                <div style="padding: 14px;">
                  <div class="userHeader">
                    <el-avatar :src="default_avater"></el-avatar>
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
                <!--icon&location here-->
                <!--i class="el-icon-location-information"></i>
                <i class="el-icon-picture-outline"></i-->
              </div>
            </el-card>
          </div>
          <!--/el-col-->
        </el-row>
      </div>
    </div>
    <!--上传图像dialog-->
    <el-dialog title="上传头像" :visible.sync="dialogVisible" width="30%">
      <el-form :model="form">
        <el-form-item :label-width="formLabelWidth" ref="uploadElement">
          <el-upload ref="upload" action="#" accept="image/png,image/gif,image/jpg,image/jpeg" list-type="picture-card"
            :limit="limitNum" :auto-upload="false" :on-exceed="handleExceed" :before-upload="handleBeforeUpload"
            :on-preview="handlePictureCardPreview" :on-remove="handleRemove" :on-change="imgChange"
            :class="{hide:hideUpload}">
            <i class="el-icon-plus"></i>
          </el-upload>
          <el-dialog :visible.sync="dialogVisible2">
            <img width="100%" :src="dialogImageUrl" alt="">
          </el-dialog>
        </el-form-item>
        <el-form-item>
          <el-button size="small" type="primary" @click="uploadFile">上传</el-button>
          <el-button size="small" @click="tocancel">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
  //for header
  import Qs from 'qs'
  import axios from "axios"
  export default {
    data() {

      return {
        default_avater: "https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png",
        ismine: true,
        tmp_username: "",
        activeIndex2: '1',
        busy: true,

        hideUpload: false,
        dialogImageUrl: '',
        dialogVisible: false, //上传窗口
        formLabelWidth: '80px',
        limitNum: 1,
        form: {},
        dialogVisible2: false, //图片预览弹窗

        searchbar: {
          input: '',
        },
        posts: []
      }
    },

    methods: {
      validateMine() {
        var tmp_username = localStorage.getItem('tmp_username');
        var fromname = this.$route.query.username;
        this.ismine = (tmp_username == fromname);
        console.log(tmp_username, fromname);
        this.tmp_username = fromname;
      },

      goBack() {
        this.$router.go(-1);
      },
      postDetail(Inp) {
        this.$router.push({
          path: '/postDetail',
          query: {
            "pid": Inp
          }
        })
      },

      //上传头像
      handleBeforeUpload(file) {
        console.log("handleBeforeUpload");
        if (!(file.type === 'image/png' || file.type === 'image/gif' || file.type === 'image/jpg' || file.type ===
            'image/jpeg')) {
          this.$notify.warning({
            title: 'warning',
            message: '请上传格式为image/png, image/gif, image/jpg, image/jpeg的图片'
          })
        }
        let size = file.size / 1024 / 1024 / 2
        if (size > 2) {
          this.$notify.warning({
            title: 'warning',
            message: '图片大小必须小于2M'
          })
        }

        let fd = new FormData();
        fd.append("image", file); //传文件
        fd.append('type', 'change_user_fig');
        fd.append('jwt', localStorage.getItem('token'));
        console.log("before axios");
        axios({
          url: "userinfo",
          method: "post",
          data: fd,
        }).then((res) => {
          console.log("uploadresis", res);
          dialogVisible2 = false;
          dialogVisible = false;
        }).catch((err) => {
          console.log(err);
        })
      },
      handleExceed(files, fileList) {

      },
      handleRemove(file, fileList) {
        this.hideUpload = fileList.length >= this.limitNum;

      },
      handlePictureCardPreview(file) {
        this.dialogImageUrl = file.url;
        this.dialogVisible2 = true;
      },
      uploadFile() {
        this.$refs.upload.submit()

      },
      imgChange(files, fileList) {
        this.hideUpload = fileList.length >= this.limitNum;
        if (fileList) {
          this.$refs.uploadElement.clearValidate();
        }
      },
      tocancel() {
        this.dialogVisible = false
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
      },

    },
    mounted: function () { //获取用户信息和用户的帖子list
      this.validateMine();
      var datas = {
        'type': 'get_user_info'
      };
      //获取头像信息
      datas['user_name'] = this.tmp_username;
      var params = Qs.stringify(datas);
      console.log(datas);
      axios({
        url: 'userinfo',
        method: 'post',
        data: params
      }).then((res) => {
        console.log(res);
        if (res.data.user_info.user_fig) {
          this.default_avater = res.data.user_info.user_fig;
        }
      }).catch((err) => {
        console.log(err);
      })
      //获取用户的帖子list
      var datas = {
        'type': 'view_posts',
        'user_name': this.tmp_username
      };
      var params = Qs.stringify(datas);
      axios({
        url: 'index',
        method: 'post',
        data: params
      }).then((res) => {
        console.log(res);
        this.add_posts(res.data.post_info_list);
      }).catch((err) => {
        console.log(err);
      })
    }
  }

</script>

<style scoped>
  .allbox {
    background-image: url("../../assets/bg_new.jpg");
    background-size: contain;
    height: 100%;
    width: 100%;
    background-position: 400px 0px;
    background-repeat: no-repeat;
    position: fixed;
  }

  .line {
    padding: 20px
  }

  .time {
    font-size: 13px;
    color: #999;
  }

  //for user
  .userInfoCard {}


  .CardList {
    height: 800px;
    overflow-y: auto;
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

  .hide .el-upload--picture-card {
    display: none;
  }

</style>
