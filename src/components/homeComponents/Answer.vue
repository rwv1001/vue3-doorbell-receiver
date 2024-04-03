<template>
  <div class="d-flex">
    <div @click="answered" class="c-item-1 m-0 justify-content-center d-flex c-answer">
      <h1 class="align-self-center c-vertical m-0 display-1 ">Answer</h1>
    </div>
    <div class="c-item-2 m-0 flex-grow-1 d-flex justify-content-center">
          <div class="d-flex align-items-center">
            <div class="d-flex flex-column">
              <div v-for="message in doormessages">
                  <h1>{{message}}</h1>
              </div>
            </div>
          </div>
    </div>

  </div>


</template>
<script setup>



</script>


<script>
var audioContext = new AudioContext();
var audioBuffer;

export default {
  name: 'AnswerPage',
  props: ['doormessages'],
  methods: {
    answered() {
      var audioElement = new Audio("http://192.168.1.47:8080/assets/4-ReplyMsg.mp3");
      //var audioSource = audioContext.createMediaElementSource(audioElement);
      //audioSource.connect(audioContext.destination);
      audioElement.playbackRate=1.5;
      audioElement.play();
      this.$emit('answered');

    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}

.c-answer:hover{
  cursor: pointer;
}

.c-item-1{
  height: 100vh;
  width:190px;
  border: 1px solid #333;
  background-color:rgb(0, 0, 0);
}
.c-item-2{
  height: 100vh;
  width:140px;
  border: 1px solid #333;
  background-color:rgb(255, 255, 255);
}

.c-vertical {
  font-weight: bold;
  color: white;
  transform: rotate(270deg);  
} 



</style>
