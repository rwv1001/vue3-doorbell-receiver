import "/css/main.min.css"
//import "bootstrap/dist/css/bootstrap.css"
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
// import Vue from 'vue';
// import VueCookies from 'vue-cookies';

// Vue.use(VueCookies, { expires: '7d'})

createApp(App).use(router).mount('#app')
console.log("hello world RWV")

import "bootstrap/dist/js/bootstrap.js"
// import { io } from "socket.io-client";
// import { ref } from "vue";
// const socket = io('ws://192.168.1.47:3500')

// export const state = ref({
//     connected: false
//   });

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

// socket.on('connect', () => {
//     console.log('connected');
//     // state.connected = true;
//     // const li = document.createElement('li')
//     // li.textContent = "connected"
//     // document.querySelector('ul').appendChild(li)
// })

// socket.on('disconnect', () => {    
//     console.log('disconnect');
//     // state.connected = false;
//     // const li = document.createElement('li')
//     // li.textContent = "disconnected"
//     // document.querySelector('ul').appendChild(li)
// })
