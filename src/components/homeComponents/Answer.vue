
<template>
  <div class="row flex-grow-1  d-flex justify-content-center align-items-center text-center bg-lightblue">
      <div class="d-flex flex-column">
              <!-- Visible only on xs  -->  
              <div v-for="message in doormessages" class="d-block d-sm-none m-0 p-0">
                  <h6>{{message}}</h6>
              </div>
              <!-- Visible only on sm  -->
               <div v-for="message in doormessages" class="d-none d-sm-block d-md-none">
                  <h5>{{message}}</h5>
              </div>
              <!-- Visible only on md  -->
               <div v-for="message in doormessages" class="d-none d-md-block d-lg-none">
                  <h5>{{message}}</h5>
              </div>
              <!-- Visible only on lg -->
               <div v-for="message in doormessages" class="d-none d-lg-block d-xl-none">
                  <h4>{{message}}</h4>
              </div>
              <!-- Visible only on xl -->
               <div v-for="message in doormessages" class="d-none d-xl-block d-xxl-none">
                  <h3>{{message}}</h3>
              </div>
              <!-- Visible only on xxl -->
               <div v-for="message in doormessages" class="d-none d-xxl-block">
                  <h2>{{message}}</h2>
              </div>
      </div>
  </div>
  <div class="row">
    <div  v-if="answering" class="col d-flex justify-content-center align-items-center  c-vh-20 bg-warning">
      <h1 class="align-self-center text-dark m-0 display-6 d-block d-sm-none">Go to door!</h1>
      <h1 class="align-self-center text-dark m-0 display-5 d-none d-sm-block d-md-none">Go to door!</h1>
      <h1 class="align-self-center text-dark m-0 display-4 d-none d-md-block d-lg-none">Go to door!</h1>
      <h1 class="align-self-center text-dark m-0 display-3 d-none d-lg-block d-xl-none">Go to door!</h1>
      <h1 class="align-self-center text-dark m-0 display-2 d-none d-xl-block d-xxl-none">Go to door!</h1>
      <h1 class="align-self-center text-dark m-0 display-1 d-none d-xxl-block">Go to door!</h1>
    </div>
    <div  v-else @click="answered" class="col d-flex justify-content-center align-items-center c-vh-20 c-answer bg-dark">
      <h1 class="align-self-center text-light m-0 display-6 d-block d-sm-none">I'll Answer</h1>
      <h1 class="align-self-center text-light m-0 display-5 d-none d-sm-block d-md-none">I'll Answer</h1>
      <h1 class="align-self-center text-light m-0 display-4 d-none d-md-block d-lg-none">I'll Answer</h1>
      <h1 class="align-self-center text-light m-0 display-3 d-none d-lg-block d-xl-none">I'll Answer</h1>
      <h1 class="align-self-center text-light m-0 display-2 d-none d-xl-block d-xxl-none">I'll Answer</h1>
      <h1 class="align-self-center text-light m-0 display-1 d-none d-xxl-block">I'll Answer</h1>
    </div>
    
    <div v-if="intercomClientId == 0 && intercomPossible"  @click="startIntercom" class="col d-flex justify-content-center align-items-center  c-vh-20 c-answer bg-success">
      <h1 class="align-self-center text-light m-0 display-6 d-block d-sm-none">Start Intercom</h1>
      <h1 class="align-self-center text-light m-0 display-5 d-none d-sm-block d-md-none">Start Intercom</h1>
      <h1 class="align-self-center text-light m-0 display-4 d-none d-md-block d-lg-none">Start Intercom</h1>
      <h1 class="align-self-center text-light m-0 display-3 d-none d-lg-block d-xl-none">Start Intercom</h1>
      <h1 class="align-self-center text-light m-0 display-2 d-none d-xl-block d-xxl-none">Start Intercom</h1>
      <h1 class="align-self-center text-light m-0 display-1 d-none d-xxl-block">Start Intercom</h1>
    </div>
    <div v-else-if="intercomRecording" @click="hangUp" class="col d-flex justify-content-center align-items-center  c-vh-20 c-answer bg-danger">
      <h1 class="align-self-center text-light m-0 display-6 d-block d-sm-none">Hang Up</h1>
      <h1 class="align-self-center text-light m-0 display-5 d-none d-sm-block d-md-none">Hang Up</h1>
      <h1 class="align-self-center text-light m-0 display-4 d-none d-md-block d-lg-none">Hang Up</h1>
      <h1 class="align-self-center text-light m-0 display-3 d-none d-lg-block d-xl-none">Hang Up</h1>
      <h1 class="align-self-center text-light m-0 display-2 d-none d-xl-block d-xxl-none">Hang Up</h1>
      <h1 class="align-self-center text-light m-0 display-1 d-none d-xxl-block">Hang Up</h1>
    </div>
    <div v-else-if="intercomPossible"  class="col d-flex justify-content-center align-items-center  c-vh-20 bg-secondary">
      <h1 class="align-self-center text-light m-0 display-6 d-block d-sm-none">Intercom in Use</h1>
      <h1 class="align-self-center text-light m-0 display-5 d-none d-sm-block d-md-none">Intercom in Use</h1>
      <h1 class="align-self-center text-light m-0 display-4 d-none d-md-block d-lg-none">Intercom in Use</h1>
      <h1 class="align-self-center text-light m-0 display-3 d-none d-lg-block d-xl-none">Intercom in Use</h1>
      <h1 class="align-self-center text-light m-0 display-2 d-none d-xl-block d-xxl-none">Intercom in Use</h1>
      <h1 class="align-self-center text-light m-0 display-1 d-none d-xxl-block">Intercom in Use</h1>
    </div>

  </div>
</template>
<script setup>



</script>


<script>

export default {
  name: 'AnswerPage',
  props: ['doormessages', 'intercomRecording', 'dataClientId', 'intercomClientId', "intercomPossible"],
  emits: ['startIntercom', 'answered', 'hangUp'],
  methods: {
    answered() {
      this.$emit('answered');
      this.answering = true;
    },
    startIntercom() {
      if(this.dataClientId != this.intercomClientId){
        console.log("Emit startIntercom")
        this.$emit('startIntercom', this.dataClientId)
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

h6 {
  font-size: 1rem; /* Smaller than the standard h6 size */
  font-weight: normal;
  margin: 0;
  padding: 0;
}
h5 {
  font-size: 2rem; /* Smaller than the standard h6 size */
  font-weight: normal;
  margin: 0;
  padding: 0;
}

.display-6{ 
  font-size: 1.3rem; /* Smaller than the standard h6 size */
  font-weight: bold;
}
.display-5{
  font-size: 1.5rem; /* Smaller than the standard h6 size */
  font-weight: bold;
}
.display-4{
  font-size: 2.3rem; /* Smaller than the standard h6 size */
  font-weight: bold;
}
.display-3{
  font-size: 2.9rem; /* Smaller than the standard h6 size */
  font-weight: bold;
}

.display-2{
  font-size: 3.8rem; /* Smaller than the standard h6 size */
  font-weight: bold;
}
.display-1{
  font-size: 4.6rem; /* Smaller than the standard h6 size */
  font-weight: bold;
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

.bg-green {
  background-color: green;
}

.bg-lightgrey {
  background-color: lightgrey;
}

.bg-lightred {
  background-color: #ff3333;
}

.bg-black {
  background-color: black;
}
.c-vh-20 {
  height: 20vh;  
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
