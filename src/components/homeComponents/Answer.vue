<template>
  <div class="d-flex">
    <div @click="updateMsg" class="c-item-1 m-0 justify-content-center d-flex">
      <h1 class="align-self-center c-vertical m-0 display-1">Answer</h1>
    </div>
    <div class="c-item-2 m-0 flex-grow-1 d-flex justify-content-center"><h1 class="align-self-center">{{statusMsg.message}}</h1></div>

  </div>


</template>
<script setup>
import {ref} from "vue";
const statusMsg = ref({ message: "Visitor for Robert"});



const updateMsg = () => {
statusMsg.value.message = 'Robert is answering!'
}



</script>


<script>
export default {
  name: 'AnswerPage',

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