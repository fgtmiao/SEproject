<template>
<div>
<!--header here-->
    <div class="allbox">
    <div class = "mainheader">
        <!--el-card class = "headercard"  :body-style="{ padding: '30px'}"-->
    <el-card class = "headercard">
        <el-divider><span class="headertext">PASS小动物照片分享平台</span></el-divider>
        <div>
        <el-input placeholder="请输入搜索内容" v-model="searchbar.input" autocomplete="off" class="searchClass">
            <el-button slot="append" icon="el-icon-search" @click="searchF()"></el-button>
        </el-input>
        </div>

    </el-card>

    </div>
        <div>
        <el-card>
        <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"></el-avatar>
        <span>this is username</span>
        </el-card>

        </div>
        <!--all post here-->
        <div class="cardlist">
        <el-card class="">

        </el-card>
        </div>
    </div>
</div>
</template>

<script>
//for header
export default {
  data() {
    
    return {
      activeIndex2: '1',
      currentDate:new Date(),
      searchbar:{
      input: '',
      },

    }
  },
  methods:{
      searchF()
      {
          //search for
        console.log(this.searchbar.input)
        
      },


      handleSelect(key, keyPath) {
        console.log(key, keyPath);
        if(key=="4"){
          this.$router.push({path:'/userinfo', query:{"userID":"this is userid"} })
        }
      } 
  }
}
</script>

<style acoped>
.headercard{
  padding-top: 30px;
  border-radius: 0px;
}
.headertext{
  color:#101010;
  font-size:30px;
}
.allbox{
  background-image:url("../../assets/bg_new.jpg");
  background-size: contain;
  height:100%;
  background-position: 400px 0px;
  background-repeat: no-repeat;
  background-attachment: fixed;
}

.searchClass{
  // position:fixed;
  border: 1px solid #c5c5c5;
  border-radius: 20px;
  background: #f4f4f4;
  margin-bottom:10px;
}
.searchClass .el-input-group__prepend {
  border: none;
  background-color: transparent;
  // padding: 0 10px 0 30px;
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
}
</style>