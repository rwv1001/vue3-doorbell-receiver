<template>
  <div id="videos">
      <video class="video-player" id="remote-video" autoplay playsinline controls></video>
  </div>
  <div class="call-div" @click="startIntercomCall"></div>


</template>


<script>

export default {
  name: 'CallPage',
  emits: ["intercomCall"],
  methods: {
    startIntercomCall() {
      this.$emit('intercomCall');
    }
  }
}
</script>

<style>
#videos{
    display: none;
    grid-template-columns: 1fr 1fr;
    gap: 2em;
    width: 600px;
    height: 600px;


    background-color: rgba(0, 0, 255, 0.3);
    position: fixed;
    top: 200px;
    left: 0px;
}

.video-player{
    background-color: black;
    width: 100%;
}

#video-wrapper{
    position: relative;
}

.call-div {
    width: 200px;
    height: 200px;
    background-color: blue;
    position: fixed;
    bottom: 0;
    right: 200px;
    cursor: pointer;
    display: none;
  }
</style>
