// const express = require('express');
// const app = express();
// const http = require('http');
// const server = http.createServer(app);
// const { Server } = require("socket.io");
// const io = new Server(server);

// app.get('/', (req, res) => {
//   res.sendFile('/home/pi/vue3-doorbell-receiver/public/test.html');
// });

// io.on('connection', (socket) => {
//   socket.on('chat message', (msg) => {
//     io.emit('chat message', msg);
//   });
// });


// server.listen(3000, () => {
//   console.log('listening on *:3000');
// });




// import { reactive } from "vue";
// import { io } from "socket.io-client";

// export const state = reactive({
//   connected: false,
//   fooEvents: [],
//   barEvents: []
// });

// // "undefined" means the URL will be computed from the `window.location` object
// const URL = process.env.NODE_ENV === "production" ? undefined : "http://localhost:3000";

// export const socket = io(URL);

// socket.on("connect", () => {
//   state.connected = true;
// });

// socket.on("disconnect", () => {
//   state.connected = false;
// });

// socket.on("foo", (...args) => {
//   state.fooEvents.push(args);
// });

// socket.on("bar", (...args) => {
//   state.barEvents.push(args);
// });

// const io = new Server({
//     cors: {
//       origin: "http://localhost:8080"
//     }
//   });
