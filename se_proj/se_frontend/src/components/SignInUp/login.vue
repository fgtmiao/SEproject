<template>
  <div class="login-container">

  <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="signin-ruleForm">
  <h2 class="login-title">PASS登录</h2>
    <el-form-item label="用户名" prop="username">
      <el-input type="username" v-model="ruleForm.username" placeholder="用户名为6～20位数字或字母" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="密码" prop="pass">
      <el-input type="password" v-model="ruleForm.pass" placeholder="必须是8～30位的字母或数组" autocomplete="off"></el-input>
    </el-form-item>

    <el-form-item>
      <el-button type="signin" @click="signIn('ruleForm')">登录</el-button>
      <el-button type="signup" @click="signUp">注册</el-button>
    </el-form-item>

  </el-form>

  </div>
</template>
  <script>
export default {
  data() {
      var checkUsername = (rule, value, callback) => {
        if (!value) {
          callback(new Error('用户名不能为空'));
        }
        else{
          var pwdRegex = new RegExp('[0-9a-zA-Z]{6,20}');
          if (!pwdRegex.test(value)){
            callback(new Error("用户名需要为包括英文或数字的6～20位字符串"));
          }
          // else if(this.ruleForm.username !== '')
          // {
          //   this.$refs.ruleForm.validateField('username');
          // }
          callback();
        }
      };
      
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'));
        } 
        else {
            var pwdRegex = new RegExp('(?=.*[0-9])(?=.*[a-zA-Z]).{8,30}');
            if (!pwdRegex.test(value)) 
            {
            callback(new Error("密码中必须包含字母、数字且为8～30位"));
            }
            // else if (this.ruleForm.pass !== '') {
            // this.$refs.ruleForm.validateField('pass');
            // // callback();
            // } 
          callback();
        }
      };

    return {
      color1: '#409EFF',
      color2: '#409EFF',
      ruleForm: {
          pass: '',
          username: '',
        },
      rules: {
        username: [
            { validator: checkUsername, trigger: 'blur' }
          ],
        pass: [
            { validator: validatePass, trigger: 'blur' }
          ],

        }
    };
  },

  methods: {

    showsuccess(that){
      that.$notify({
        title: '登录成功',
        message: '',
        type: 'success'
        });
      },


    signIn(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            // alert('submit!');
            this.$options.methods.showsuccess(this);
            this.$router.push({path:'/mainposts', query:{} })
          } 
          else {
            console.log('error submit!!');
            return false;
          }
        });
    },

    signUp(){
      console.log("signup")
      this.$router.push({path:'signup', query:{ test:"asdasd" } })
    },
    submitUserLogin(){

    },
    checkUserLogin(){

    }
  }
};
</script>

<style acoped>

.signin-ruleForm {
  width: 350px;
  margin: 160px auto; /* 上下间距160px，左右自动居中*/
  background-color: rgb(255, 255, 255, 0.8); /* 透明背景色 */
  padding: 30px;
  border-radius: 20px; /* 圆角 */
}

.login-form {
  width: 350px;
  margin: 160px auto; /* 上下间距160px，左右自动居中*/
  background-color: rgb(255, 255, 255, 0.8); /* 透明背景色 */
  padding: 30px;
  border-radius: 20px; /* 圆角 */
}

/* 背景 */
.login-container {
  position: absolute;
  width: 100%;
  height: 100%;
  background: url("../../assets/bg2.jpg");
  background-size: cover;
}

/* 标题 */
.login-title {
  color: #303133;
  text-align: center;
}
.el-button--signin{background: #23C6C8;}
.el-button--signup{background: #FCB065;}

</style>