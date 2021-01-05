<template>
  <div class="logup-container">

    <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="signup-ruleForm">
      <el-form-item label="用户名" prop="username">
        <el-input type="username" v-model="ruleForm.username" placeholder="用户名支持数字字母汉字下划线" autocomplete="off">
        </el-input>
      </el-form-item>
      <el-form-item label="密码" prop="pass">
        <el-input type="password" v-model="ruleForm.pass" placeholder="必须是8～30位的字母或数字" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="确认密码" prop="checkPass">
        <el-input type="password" v-model="ruleForm.checkPass" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="电子邮箱" prop="email">
        <el-input class="reg" type="email" v-model="ruleForm.email" placeholder="example@gamil.com"></el-input>
      </el-form-item>
      <!--el-form-item label="年龄" prop="age">
    <el-input v-model.number="ruleForm.age"></el-input>
  </el-form-item-->
      <el-form-item>
        <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
        <el-button @click="resetForm('ruleForm')">返回登录</el-button>
      </el-form-item>
    </el-form>

  </div>
</template>

<script>
  import Qs from 'qs'
  import axios from "axios"
  import crypto from 'crypto'
  export default {
    data() {
      var checkUsername = (rule, value, callback) => {
        if (!value) {
          return callback(new Error('用户名不能为空'));
        } 
        else {
          //去除用户名限制
          var nickRegex = new RegExp('^[a-zA-Z0-9_\u4e00-\u9fa5]+$');
          if (!nickRegex.test(value)) {
            callback(new Error("用户名只支持为汉字英文数字下划线！"));
          }
          //  check重名
          callback();
        }
      };
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'));
        } else {
          var pwdRegex = new RegExp('(?=.*[0-9])(?=.*[a-zA-Z]).{8,30}');
          if (!pwdRegex.test(value)) {
            callback(new Error("密码中必须包含字母、数字且为8～30位"));
          } else {
            if (this.ruleForm.pass !== '') {
              this.$refs.ruleForm.validateField('checkPass');
            }
            callback();
          }
          callback();
        }
      };
      var validatePass2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'));
        } else if (value !== this.ruleForm.pass) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback();
        }
      };

      var checkEmail = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请填写邮箱'));
        } else {
          var reg = new RegExp("^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$");
          if (!reg.test(value)) {
            callback(new Error('请输入有效的邮箱'));
          }
          callback();
        }
      };

      return {
        ruleForm: {
          pass: '',
          checkPass: '',
          username: '',
          email: '',
        },
        rules: {
          pass: [{
            validator: validatePass,
            trigger: 'blur'
          }],
          checkPass: [{
            validator: validatePass2,
            trigger: 'blur'
          }],
          username: [{
            validator: checkUsername,
            trigger: 'blur'
          }],
          email: [{
            validator: checkEmail,
            trigger: 'blur'
          }]
        }
      };
    },

    methods: {
      showsuccess(that) {
        that.$notify({
          title: '注册成功！',
          message: '',
          type: 'success'
        });
      },
      showfail(that, msg) {
        that.$notify.error({
          title: '注册失败',
          message: msg,
        });
      },
      submitForm(formName) {
        this.$refs[formName].validate((formvalid) => {
          if (formvalid) {
            //send post
            console.log("注册账号和密码为")
            console.log(this.ruleForm.username)
            
            //在此处进行加密算法
            var md5 = crypto.createHash("md5")
            md5.update(this.ruleForm.pass)//this.pw2这是你要加密的密码
            var pw = md5.digest('hex')
            console.log(pw)
            var datas = {
              'type': 'signup',
              'user_name': this.ruleForm.username,
              // 'password': this.ruleForm.pass
              'password':pw,
            };
            var params = Qs.stringify(datas);
            let _this = this;
            axios({
              // url: 'http://8.131.74.16/index',
              url: 'index',
              method: 'post',
              data: params
            }).then((res) => {
              console.log("res from server")
              console.log(res)
              if (res.data.succ) {
                //本地保存token
                // _this.userToken=res.data.token;
                // console.log(_this.userToken)
                localStorage.setItem('token', res.data.token);
                localStorage.setItem('tmp_username', this.ruleForm.username);

                console.log(localStorage.getItem('token'));
                this.$options.methods.showsuccess(this);
                this.$router.push('/mainposts');
              } else { //failed用户名重复
                this.$options.methods.showfail(this, "用户名已存在");
                console.log(res.data.errmsg)
              }
            }).catch((error) => {
              this.$options.methods.showfail(this, "网络错误");
              console.log("error", error)
            })

          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },

      resetForm(formName) {
        this.$refs[formName].resetFields();
        this.$router.push('/');
      },

    }
  }

</script>

<style scoped>
  .signup-ruleForm {
    width: 350px;
    margin: 160px auto;
    /* 上下间距160px，左右自动居中*/
    background-color: rgb(255, 255, 255, 0.8);
    /* 透明背景色 */
    padding: 30px;
    border-radius: 20px;
    /* 圆角 */
  }

  .logup-container {
    position: absolute;
    width: 100%;
    height: 100%;
    background: url("../../assets/bg2.jpg");
    background-size: cover;
  }

</style>
