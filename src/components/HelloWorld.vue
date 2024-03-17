<template>
  <div class="d-flex">
    <div @click="updateMsg" class="c-item-1 m-0 justify-content-center d-flex">
      <h1 class="align-self-center c-vertical m-0 display-1">Answer</h1>
    </div>
    <div class="c-item-2 m-0 flex-grow-1 d-flex justify-content-center"><h1 class="align-self-center">{{statusMsg.message}}</h1></div>

  </div>
  <div class="c-topright d-flex">
    <h6 v-show="showUser" class="p-3">{{ currentUser.userName }}</h6>
    <div class="c-item m-0">
      <nav class="navbar bg-light">
        <div class="container-fluid">

          <button @click="toggleUser" class="navbar-toggler ms-auto" type="button" data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
            aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="list-group">
           
              <li v-for="user in users" :key="user.id" :class="{active: user.userName===currentUser.userName, shun}" class="list-group-item" @click="updateUser(user.userName)">{{user.userName}}</li>
            </ul>

          </div>
        </div>
      </nav>

    </div>
  </div>

</template>
<script setup>
import {ref} from "vue";
const statusMsg = ref({ message: "Visitor for Robert"});
const showUser = ref(true);
const currentUser = ref({userName: 'Fr Robert'})
const users = ref([{ userName: 'General'},{userName:'Fr Robert'},{userName:'Fr Greg'}, {userName:'Fr Albert'}])

const updateMsg = () => {
statusMsg.value.message = 'Robert is answering!'
}
const updateUser = (newUserName) => {
  console.log(newUserName);
  currentUser.value.userName = newUserName
}

const toggleUser = () => {
  showUser.value=!showUser.value;
}
</script>


<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
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
.c-item {
  
  border: 1px solid #333;
  background-color:rgb(176, 190, 136);
  
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

.c-topright {
  position: absolute;
  top: 0px;
  right: 0px;
}

</style>