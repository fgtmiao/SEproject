
<template>
<div>
<!--header-->
<el-page-header @back="goBack" content="发布帖子">
</el-page-header>
<!--main content-->
<el-card>
<div class="width100Precent">
<el-input
  type="textarea"
  :autosize="{ minRows: 2, maxRows: 4}"
  placeholder="请输入内容"
  v-model="description">
</el-input>
    <div class="uploadIMG uploadSty"  v-if="dialogTitle!=='查看'">
        <el-upload
                                    action="#"
                                    ref="upload"
                                    multiple
                                    list-type="picture-card"
                                    :auto-upload="false"
                                    accept=".jpeg,.jpg,.png,"
                                    :file-list="fileLists"
                                    :on-preview="handlePictureCardPreview"
                                    :limit="9"
                                    :on-change="OnChange"
                                    :on-remove="handleRemove"
                                    :class="{disUoloadSty:hideUploadEdit}"
                                   >
                                    <i slot="default" class="el-icon-plus"></i>
        </el-upload>
        <p>注：最多上传9张图片</p>
    </div>
    <div class="uploadIMG uploadSty"  v-if="dialogTitle=='查看'" >
        <div class="demo-image__preview">
                                <el-image v-if="previewList.length==0">
                                        <div slot="error" class="image-slot">
                                            <i class="el-icon-picture-outline"></i>
                                        </div>
                                </el-image>
        <el-image v-else class="elImageSty" v-for="(item,index) in previewList" :src="item"  :key="index" fit="contain" lazy :preview-src-list="getPreviewImgList(index)"></el-image>
        </div>
    </div>
</div>

  <el-select
    v-model="value"
    multiple
    filterable
    allow-create
    default-first-option
    placeholder="请选择或输入动物种类">
    <el-option
      v-for="item in options"
      :key="item.value"
      :label="item.label"
      :value="item.value">
    </el-option>
  </el-select>
  <!--这里就直接列出所有动物吧，怎么上传位置啊-->
    <el-button @click="submit()">
    发布
    </el-button>
    </el-cascader>

　　<el-dialog :visible.sync="dialogImgVisible" title="图片">
    　　<img width="100%" :src="dialogImageUrl" alt="">
　　</el-dialog>

<!--class & locations-->

</el-card>
</div>
</template>


<script>
import Qs from 'qs'
import axios from "axios"

export default {
    
  data(){
      return{
        description: '',
        dialogImgVisible: false,////大图预览框
        hideUploadEdit:false,//图片个数设置 超过5张为true
        options: [{
          value: '猫咪',
          label: '猫咪'
        }, {
          value: '刺猬',
          label: '刺猬'
        }, {
          value: '喜鹊',
          label: '喜鹊'
        }, {
          value: '麻雀',
          label: '麻雀'
        }, {
          value: '鸳鸯',
          label: '鸳鸯'
        }, {
          value: '天鹅',
          label: '天鹅'
        }, {
          value: '鱼',
          label: '鱼'
        }],
        value: []
      };
  },
  methods:{
    goBack(){
      this.$router.go(-1);
    },
    OnChange (file, fileList) {//上传之前检查
      console.log(file)
      var testmsg = file.name.substring(file.name.lastIndexOf('.')+1)
      const extension = testmsg === 'jpeg'
      const extension2 = testmsg === 'jpg'
      const extension3 = testmsg === 'png'
      const isLt2M = file.size / 1024 / 1024 < 10
      if(!isLt2M){
        this.$message({
          type: 'warning',
          message: '文件大小请限制在10M以内'
        });
      }
      if(!extension && !extension2 && !extension3) {
        this.$message({
          message: '上传文件只能是 jpeg、jpg、png格式!',
          type: 'warning'
        });
      }
      this.fileLists.push(file)
      this.hideUploadEdit = fileList.length >= 5
      return (extension || extension2 || extension3)  && isLt2M;
    },
    handlePictureCardPreview(file){
        var _this = this;
        _this.dialogImgVisible = true;　　　　　　　　　　//这里项目中做了弹框设置，判断是新选择的图片url 还是已经存在的图片url
        if(file.raw){
          _this.dialogImageUrl = file.url;
        }else{
          _this.dialogImageUrl = file.urls;
        }
    },
//修改-删除图片
    handleRemove(file, fileList) {
      var _this = this
      _this.fileLists = fileList
      _this.hideUploadEdit = fileList.length >= 5
    },
    getPreviewImgList:function(index) {
      let arr = []
      let i = 0;
      for(i;i < this.previewList.length;i++){
        arr.push(this.previewList[i+index])
        if(i+index >= this.previewList.length-1){
          index = 0-(i+1);
        }
      }
      return arr;
    }, 
    submit() {
      console.log(this.description);
      console.log(this.value);
      if (!this.description) {
        this.$message({
          showClose: true,
          type:'warning',
          message:'帖子正文不能为空'
        });
      } else {
        var datas = {
          'type': 'add_post', 'jwt': localStorage.getItem('token'),
          'post[description]': this.description
        }
        var params = Qs.stringify(datas);
        console.log(datas, params);
        axios({url: 'index', method: 'post', data: params}, )
          .then((res) => {
            if (res.data.succ) {
              console.log('succ', res.data);
              this.$notify({
                type:'success',
                title:'帖子发布成功'
              });
            }
            else {
              console.log("res_error", res);
            }
          })
          .catch((err) => {
            console.log("catch_error", err);
          });
      }
    }
  }
}
</script>

<style scoped>
</style>