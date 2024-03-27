<template>
  <NavMenu  :currentUser="currentUser" :users="users" @updateUser="updateUser" @finish="finish" />  
  <AnswerPage v-if="justRang"  />
  <BaseConnection :connected="con"/>
  <!-- <DisplayTime />   -->

</template>

<script>
import NavMenu from './components/NavMenu.vue'
import AnswerPage from './components/Answer.vue'
// import DisplayTime from './components/DisplayTime.vue'
import BaseConnection from './components/BaseConnection.vue'
import { io } from "socket.io-client";
import { ref } from "vue";
const socket = io('ws://192.168.1.47:3500')

 const connected = ref(true);

// function sendMessage(e) {
//     e.preventDefault()
//     const input = document.querySelector('input')
//     if (input.value) {
//         socket.emit('message', input.value)
//         input.value = ""
//     }
//     input.focus()
// }

// // document.querySelector('form')
// //     .addEventListener('submit', sendMessage)

// // Listen for messages 
// socket.on("message", (data) => {
//     // const li = document.createElement('li')
//     // li.textContent = data
//     // document.querySelector('ul').appendChild(li)
// })






export default {
  name: 'App',
  components: {
    AnswerPage, 
    NavMenu,
    // DisplayTime,
    BaseConnection
  },
  mounted() {
    socket.on('connect', () => {
    console.log('App.vue connected');
    this.con = true;
    // const li = document.createElement('li')
    // li.textContent = "connected"
    // document.querySelector('ul').appendChild(li)
})
socket.on('disconnect', () => {    
  console.log('App.vue disconnected');
    this.con = false;
    // const li = document.createElement('li')
    // li.textContent = "disconnected"
    // document.querySelector('ul').appendChild(li)
})
  },
  data() {
    return {
      justRang: false,
      con: false,
      currentUser: 'Fr Robert',
      users: [  'Generalt','Fr Robert','Fr Greg','Fr Albert' ]
    }
  },
  methods: {
    updateUser(newUserName) {
      console.log('Update aaaaa' )
      this.currentUser = newUserName;     
    },
    finish(interval) {
      console.log("App Finish id: "+interval)
      clearInterval(interval);
      
    }

  }
}
</script>

<style >
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;

}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #070707;
  margin-top: 0px;
}
body {
  overflow: hidden; /* Hide scrollbars */
}

</style>
