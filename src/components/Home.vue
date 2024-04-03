<template>
  <div id="home">
    <NavMenu :currentUserId="currentUserId" :currentUserName="currentUserName" @updateUser="updateUser"
      @finish="finish" />
    <AnswerPage v-if="doormessages.length" :doormessages="doormessages" @answered="answered" />
    <BaseConnection :connected="con" :answering="doormessages.length>0" :soundAlert="soundAlertStatus" @toggleSoundAlert="toggleSoundAlert"/>
    <DisplayTime v-show="doormessages.length == 0" />
    <router-view />
  </div>
</template>

<script>
import NavMenu from './homeComponents/NavMenu.vue'
import AnswerPage from './homeComponents/Answer.vue'
import DisplayTime from './homeComponents/DisplayTime.vue'
import BaseConnection from './homeComponents/BaseConnection.vue'
import { io } from "socket.io-client";
import { ref } from "vue";
import { useCookies } from "vue3-cookies";
const io_connection = io('ws://192.168.1.47:3500')

const connected = ref(true);

export default {
  name: 'Home',
  components: {
    AnswerPage,
    NavMenu,
    DisplayTime,
    BaseConnection
  },
  setup() {
    const { cookies } = useCookies();
    return { cookies };
  },
  mounted() {
    let my_cookie_user = this.cookies.get("currentUsesr");
    if(my_cookie_user != null) {
      this.currentUserName = my_cookie_user.name;
      this.currentUserId = my_cookie_user.id;
    }
    console.log("Cookie user: "+ my_cookie_user);

    io_connection.on('connect', (socket) => {
      console.log('App.vue connected');
      this.con = true;      
    })
    io_connection.on('message_list', (message_uuid, message_list,  mp3_message_to_browser, user_generator) => {
          console.log('received_message list, uuid = ' + message_uuid);
          if(this.current_message_uuid != message_uuid) {
             this.current_message_uuid = message_uuid;
             this.doormessages = message_list;
             if(user_generator != this.currentUserId) {
               let url = "http://192.168.1.47:8080/assets/"+mp3_message_to_browser;
               console.log("Try to play the mp3: "+ url)
               if(this.soundAlertStatus) {
                 var audioElement = new Audio(url);
                 audioElement.playbackRate=1.5;
                 audioElement.play();
               }
             }
   
          }
    })
    io_connection.on('doorbell_idle', () => {
          console.log('doorbell idle');
          this.doormessages = [];
    })
    io_connection.on('disconnect', () => {
      console.log('App.vue disconnected');
      this.con = false;
    })
  },
  data() {
    return {
      justRang: false,
      doormessages: [],
      current_message_uuid: 0,
      con: false,
      currentUserId: 1,
      currentUserName: '',
      soundAlertStatus: false
    }
  },
  methods: {
    updateUser(newUserId, newUserName) {
      console.log('Update aaaaa')
      this.currentUserId = newUserId;
      this.currentUserName = newUserName
      var user = { id:this.currentUserId, name:this.currentUserName}; 
      this.cookies.set("currentUsesr", user, "30d");
    },
    finish(interval) {
      console.log("App Finish id: " + interval)
      clearInterval(interval);

    },
    answered() {
      console.log("Answered clicked by "+ this.currentUserName);
      io_connection.emit('answered', this.currentUserId)
    },
    toggleSoundAlert() {
      this.soundAlertStatus = !this.soundAlertStatus;
      console.log("soundAlertStatus = " + this.soundAlertStatus);
    }

  }
}
</script>

<style>
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

#home {
  overflow: hidden;
  /* Hide scrollbars */
}
</style>
