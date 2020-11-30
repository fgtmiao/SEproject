<template>
<div class="logup-container">

<el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="signup-ruleForm">
  <el-form-item label="用户名" prop="username">
    <el-input type="username" v-model="ruleForm.username" placeholder="用户名为6～20位数字或字母" autocomplete="off"></el-input>
  </el-form-item>
  <el-form-item label="密码" prop="pass">
    <el-input type="password" v-model="ruleForm.pass" placeholder="必须是8～30位的字母或数组" autocomplete="off"></el-input>
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
  export default {
    data() {
      var checkUsername = (rule, value, callback) => {
        if (!value) {
          return callback(new Error('用户名不能为空'));
        }
        else{
          var nickRegex = new RegExp('[0-9a-zA-Z]{6,20}');
          if (!nickRegex.test(value)){
            callback(new Error("用户名需要为包括英文或数字的6～20位字符串"));
          }
//  check重名
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
            else{
            if (this.ruleForm.pass!== '') {
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

      var checkEmail  = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请填写邮箱'));
        } else {
            var reg=new RegExp("^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$");
            if(!reg.test(value))
            {
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
          email:'',
        },
        rules: {
          pass: [
            { validator: validatePass, trigger: 'blur' }
          ],
          checkPass: [
            { validator: validatePass2, trigger: 'blur' }
          ],
          username: [
            { validator: checkUsername, trigger: 'blur' }
          ],
          email:[
            { validator: checkEmail, trigger: 'blur' }
          ]
        }
      };
    },

    methods: {
      showsuccess(that){
      that.$notify({
        title: '登录成功',
        message: '这是一条成功的提示消息',
        type: 'success'
        });
      },
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            //submmit here！
            alert('submit!');
            this.$options.methods.showsuccess(this);
            this.$router.push('/')
          }
          else {
            
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

<style acoped>
.signup-ruleForm {
  width: 350px;
  margin: 160px auto; /* 上下间距160px，左右自动居中*/
  background-color: rgb(255, 255, 255, 0.8); /* 透明背景色 */
  padding: 30px;
  border-radius: 20px; /* 圆角 */
}

.logup-container{ 
  position: absolute;
  width: 100%;
  height: 100%;
  background: url("../../assets/bg2.jpg");
  background-size: cover;
}
</style>