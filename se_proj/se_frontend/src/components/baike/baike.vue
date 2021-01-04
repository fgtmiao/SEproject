<template>
  <!--不复用,先只显示地理位置吧-->
  <div class="allbox">


    <div>
    <el-page-header @back="goBack" content="类别位置热度">
    </el-page-header>
    <span>This is Baike for {{map_dict[type]}}</span>
    <span>以下为地理位置分布图</span>
  <div class="test" style="background-color: #FFFFFF;">
    <canvas id="myCanvas" ref="myCanvas"
            width="1500" height="1000">
    </canvas>
  </div>
</div>

  </div>
</template>

<script>
  import axios from "axios"
  import Qs from 'qs'
  export default {

    data() {
      return {
        type: this.$route.query.type,
        //ask from 
        map_dict:{
        "3-1":"猫咪",
        "3-2":"刺猬",
            // <el-submenu index="3-3">
              // <template slot="title">鸟类</template>
        "3-4-1":"喜鹊",
        "3-4-2":"麻雀",
        "3-4-3":"鸳鸯",
        "3-4-4":"天鹅",
        "3-4":"鱼",
        }
      }
    },
    methods: {
      goBack() {
        this.$router.go(-1);
      },

      get_allpos(animal_class){
        // animal_class

        const requestFD = new FormData();
        requestFD.append('type','get_location');
        requestFD.append('animal_class', animal_class);
        
        // var params = Qs.stringify(datas);
        axios({
            url: 'index',
            method: 'post',
            data: requestFD
          }).then((res) => {
            if (res.data.succ) {
              console.log('succ', res.data);
              var poslist = res.data.pos;
              console.log(poslist);
              for(var pos of poslist)
              {
                console.log(pos);
                this.drawRect(pos);
              }
            } else {
              console.log("res_error", res);
            }
          })
          .catch((err) => {
            console.log("catch_error", err);
          });
      },
      drawRect(position){
          const canvas = this.$refs.myCanvas;
          var ctx = canvas.getContext("2d");
          let pos = position.split(",");
          let x=pos[0];
          let y=pos[1];
          // ctx.clearRect(0,0,canvas.width,canvas.height);
          ctx.strokeStyle = '#ff0000';
          ctx.lineWidth = 2;
          console.log("drawing");
          console.log(x,y);
          ctx.strokeRect(Math.max(x-10,0),Math.max(y-10,0),20,20);
      },
    },

    mounted:function(){
        // drawRect all here
      // var position = this.$route.query.position;
      // console.log(position);
      // this.drawRect(position);
      console.log(this.map_dict[this.type]);
      this.get_allpos(this.map_dict[this.type]);
    }
  }

</script>

<style scoped>

  #myCanvas{
    background-color: forestgreen;
    background-image:url('../../assets/map2.jpg');
    background-size:100%;
  }

</style>
