<template>
  <div>
    <el-page-header @back="goBack" content="位置详情">
    </el-page-header>

    <div class="test" style="background-color: burlywood;">
      <canvas id="myCanvas" ref="myCanvas" width="1500" height="1000">
      </canvas>
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        // flag: false,
        // position: this.$route.query.position
      };
    },
    methods: {
      goBack() {
        this.$router.go(-1);
      },

      drawRect(position) {
        const canvas = this.$refs.myCanvas;
        var ctx = canvas.getContext("2d");
        let pos = position.split(",");
        let x = pos[0];
        let y = pos[1];
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.strokeStyle = '#ff0000';
        ctx.lineWidth = 2;
        console.log("drawing");
        console.log(x, y);
        ctx.strokeRect(Math.max(x - 10, 0), Math.max(y - 10, 0), 20, 20);
      },

    },
    mounted: function () {
      // drawRect
      var position = this.$route.query.position;
      console.log(position);
      this.drawRect(position);
    }
  };

</script>

<style scoped>
  #myCanvas {
    background-color: forestgreen;
    background-image: url('../../assets/map2.jpg');
    background-size: 100%;
  }

</style>
