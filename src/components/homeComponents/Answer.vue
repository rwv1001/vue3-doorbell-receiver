<template>
  <div class="d-flex">
    <div v-if="answering" class="c-item-1 m-0 justify-content-center  d-flex bg-warning">
      <h1 class="align-self-center c-vertical text-dark m-0 display-4 ">Go to door!</h1>
    </div>
    <div v-else  @click="answered" class="c-item-1 m-0 justify-content-center d-flex c-answer bg-dark">
      <h1 class="align-self-center c-vertical text-light m-0 display-4 ">Answer</h1>
    </div>

    <div v-if="intercomPossible">
    <div v-if="intercomClientId == 0"  @click="startIntercom" class="c-item-1 m-0 justify-content-center d-flex c-answer bg-success">
      <h1 class="align-self-center c-vertical text-light m-0 display-4 ">Start Intercom</h1>
    </div>

    <div v-else-if="intercomClientId == dataClientId" @click="hangUp" class="c-item-1 m-0 justify-content-center d-flex c-answer bg-danger">
      <h1 class="align-self-center c-vertical text-light m-0 display-4 ">Hang Up</h1>
    </div>
    <div v-else class="c-item-1 m-0 justify-content-center d-flex bg-secondary">
      <h1 class="align-self-center c-vertical text-light m-0 display-4 ">Intercom in Use</h1>
    </div>
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

export default {
  name: 'AnswerPage',
  props: ['doormessages', 'dataClientId', 'intercomClientId', "intercomPossible"],
  methods: {
    answered() {
      this.$emit('answered');
      this.answering = true;
    },
    startIntercom() {
      if(this.dataClientId != this.intercomClientId){
        this.$emit('startIntercom', this.dataClientId)
        console.log("one possibility");
      } else {
        console.log("Someone is already using the intercom")
      }
    },
    hangUp() {
       this.$emit('hangUp')
    }
  },
  data() {
    return {
      answering: false
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
}
.c-item-answer-background {
  background-color:rgb(0, 0, 0);
}

.c-item-answering-background {
  background-color:rgb(0, 0, 0);
}

.c-item-intercom


.c-item-2{
  height: 100vh;
  width:140px;
  border: 1px solid #333;
  background-color:rgb(255, 255, 255);
}

.c-vertical {
  font-weight: bold;
  transform: rotate(270deg);  
} 



</style>
