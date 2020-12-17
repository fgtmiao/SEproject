<template>
  <!--不复用-->
  <div class="allbox">
    <span>This is Baike for {{type}}</span>

  </div>
</template>

<script>
  export default {

    data() {
      return {
        type: this.$route.query.type

      }
    },
    methods: {

    }
  }

</script>

<style scoped>
</style>
