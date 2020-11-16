<template>
  <div class="login-container">

    <el-form ref="form" :model="form" label-width="80px" class="login-form">
    
      <h2 class="login-title">管理系统</h2>
      
      <el-form-item label="userName">
        <el-input v-model="form.username"></el-input>
      </el-form-item>

      <el-form-item label="password">
        <el-input v-model="form.password"></el-input>
      </el-form-item>

      <el-form-item>
        <el-button type="signin" @click="signIn">登录</el-button>
        <el-button type="signup" @click="signUp">注册</el-button>
      </el-form-item>
    
    </el-form>

  </div>
</template>
  <script>
export default {
  data() {
    return {
      color1: '#409EFF',
      color2: '#409EFF',

      form: {
        username: "",
        password: ""
      }
    };
  },
  methods: {
    signIn() {
      console.log("signin");
    },
    signUp(){
      console.log("signup")
    }
  }
};
</script>

<style acoped>
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
  background: url("../assets/Jhin.jpg");
  
}

/* 标题 */
.login-title {
  color: #303133;
  text-align: center;
}
.el-button--signin{background: #23C6C8;}
.el-button--signup{background: #FCB065;}

</style>