<template>
 <div>
  <comment-message @handleReply="handleReply" :commentList="comments"></comment-message>
  <comment-area @reload="reload" :parentMsgId="replyMsgId" :replyMsgUsername="replyMsgUsername"></comment-area>
 </div>
</template>

<script>
import CommentMessage from "for_comment/CommentMessage";
import CommentArea from "for_comment/CommentArea";

import { findAllMsg } from "network/ajax";

export default {
 name: "Message",
 components: {
  CommentMessage,
  CommentArea
 },
 data() {
  return {
   comments: [],
   replyMsgId: "",
   replyMsgUsername: ""
  };
 },
 mounted() {
  findAllMsg()
   .then(res => {
    this.comments = res.data.messages;
   })
   .catch(err => {
    console.log(err);
    this.$router.push("/500");
   });
 },
 methods: {
  handleReply(data) {
   this.replyMsgId = data.msgId;
   this.replyMsgUsername = data.msgUsername;
  },
  reload() {
   this.$emit("reload")
  }
 }
};
</script>

<style>
</style>