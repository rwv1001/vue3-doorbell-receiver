<template>
  <div id="home">
    <NavMenu :currentUserId="currentUserId" :currentUserName="currentUserName" @updateUser="updateUser"
      @finish="finish" />
    <AnswerPage v-if="doormessages.length" :doormessages="doormessages" @startIntercom="startIntercom" @answered="answered" @hangUp="hangUp" :clientId="clientId" :intercomClientId="intercomClientId"/>
    <BaseConnection :connected="con" :answering="doormessages.length>0" :soundAlert="soundAlertStatus" @toggleSoundAlert="toggleSoundAlert"/>
    <DisplayTime v-if="doormessages.length == 0" />
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
import moment from 'moment';
import { uuid } from 'vue-uuid'
//const io_connection = io('https://socket.cambdoorbell.duckdns.org',{
//  cert: process.env.VUE_APP_SSL_CERT,
//  key: process.env.VUE_APP_SSL_KEY,
//  path: '/socket',
//  reconnection: true,
//  transport: ['websocket', 'polling'],
//  reconnectionAttempts: 5,
//})

//const io_connection = io('https://socket.cambdoorbell.duckdns.org')

const io_connection = io("https://socket.cambdoorbell.duckdns.org");


const HEART_BEAT = 2000;
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
    console.log('Home.vue has mounted - process.env:')
    console.log(process.env.VUE_APP_SSL_KEY)
    console.log(process.env.VUE_APP_SSL_CERT)
    console.log(process.env.VUE_APP_ROOT_URL)
    let my_cookie_user = this.cookies.get("currentUsesr");
    if(!this.beatInterval){
       this.beatInterval = setInterval(()=> {
          let now = new Date()
          let timeDiff = moment.duration(Date.parse(this.nextBeat)- now)
          console.log("beat timeDiff from now =  "+ timeDiff)
          if(timeDiff < 0){
            this.con = false 
          } else {
            this.con = true;
          }
       }, HEART_BEAT)
    }

    if(my_cookie_user != null) {
      this.currentUserName = my_cookie_user.name;
      this.currentUserId = my_cookie_user.id;
    }
    console.log("Cookie user: "+ my_cookie_user);
    this.clientId = uuid.v4();  
    io_connection.on('connect', (socket) => {
      console.log('App.vue connected');
     // this.con = true;      
    })
    io_connection.on('message_list', (message_uuid, message_list,  mp3_message_to_browser, user_generator, newIntercomClientId) => {
          console.log('received_message list, uuid = ' + message_uuid);
          if(this.intercomClientId != newIntercomClientId) {
             this.intercomClientId = newIntercomClientId;
             console.log('client id is: '+ this.clientId)
             console.log('intercom client id is: '+ this.intercomClientId)
          }
          if(this.current_message_uuid != message_uuid) {
             this.current_message_uuid = message_uuid;
             this.doormessages = message_list;
             console.log("user generator is "+user_generator + ", and current UserID is " +  this.currentUserId);
             if(user_generator != this.currentUserId) {
               let url = "https://assets.cambdoorbell.duckdns.org/assets/"+mp3_message_to_browser;
               console.log("Try to play the mp3: "+ url)
               if(this.soundAlertStatus) {
                 var audioElement = new Audio(url);
                 audioElement.playbackRate=1.5;
                 audioElement.play();
               }
             }
   
          }
    })
    io_connection.on('heart_beat', () => {
       this.nextBeat = moment().add(2*HEART_BEAT, 'milliseconds');
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
      soundAlertStatus: false,
      nextBeat: new Date(),
      beatInterval: null,
      clientId: -1,
      intercomClientId: 0
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
      if (navigator.mediaDevices.getUserMedia) {
           console.log("The mediaDevices.getUserMedia() method is supported.");
      }

    },
    startIntercom(clientId) {
     //this.intercomClientId = clientId;
     console.log("startIntercom called with clientId: "+ clientId)
     io_connection.emit('updateIntercomClientId',clientId, this.currentUserId ); 
    },
    hangUp() {
     io_connection.emit('updateIntercomClientId',0, this.currentUserId);
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
