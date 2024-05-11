<template>
    <div class="container">
        <div class="row mb-3 mt-3 justify-content-md-center">
            <div id="user-name"></div>
            <button id="call" class="btn btn-primary col-1">Call!</button>
            <button id="hangup" class="col-1 btn btn-primary">Hangup</button>
            <div id="answer" class="col"></div>
        </div>
        <div id="videos">
            <div id="video-wrapper">
                <div id="waiting" class="btn btn-warning">Waiting for answer...</div>
                <video class="video-player" id="local-video" autoplay playsinline controls></video>
            </div>
            <video class="video-player" id="remote-video" autoplay playsinline controls></video>
        </div>
    </div>
</template>

<script>
import { io } from "socket.io-client";
const userName = "Rob-"+Math.floor(Math.random() * 1000000)
const password = "x";
const socket = io("https://socket.cambdoorbell.duckdns.org", {
    auth: {
        userName,password
    }
});

export default {
  name: 'Intercom',
  props: {
    msg: String
  },
  methods: {
  },
  data () {
    return {
      dbSettings: []
    }
  },
  mounted() {

  }
}
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#videos{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2em;
}

.video-player{
    background-color: black;
    width: 100%;
}

#video-wrapper{
    position: relative;
}

#waiting{
    display: none;
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    margin: auto;
    width: 240px;
    height: 40px;

}

#answer{
    
}
</style>

