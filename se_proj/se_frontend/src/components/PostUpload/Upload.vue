
<!--
vue的父子组件没啥必要，待续debug
-->
<template>
  <div id="dynamic_create">
    <mt-field  v-model="dynamicContent" :placeholder="lang.dynamic_moments_thought" type="textarea" rows="4" ></mt-field>
    <uploader @getFiles='getImageList' @removeFiles='removeImage'></uploader>
    <div class="btn-wrapper">
        <!-- <mt-button class='btn-send' size="large" type="primary" @click="send">{{this.lang.dynamic_release}}</mt-button> -->
        <load-button :class="isSubmit ? 'text-666 btn-send' : 'bg-blue text-white btn-send'" :loading="isSubmit" @callback="send" :text="lang.dynamic_release"></load-button>
    </div>
  
  </div>
</template>

<script>
import 

</script>

<style acoped>
</style>