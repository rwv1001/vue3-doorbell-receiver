 <template>
  <div id="home">
    <NavMenu :currentUserId="currentUserId" :currentUserName="currentUserName" @updateUser="updateUser"
      @finish="finish" />
    <AnswerPage v-if="doormessages.length" :doormessages="doormessages" @startIntercom="startIntercom" @answered="answered" @hangUp="hangUp" :dataClientId="dataClientId" :intercomClientId="intercomClientId" :intercomPossible="intercomPossible"/>
    <BaseConnection :connected="con" :answering="doormessages.length>0" :soundAlert="soundAlertStatus" @toggleSoundAlert="toggleSoundAlert"/>
    <DisplayTime v-if="doormessages.length == 0" />
    <CallPage @intercomCall="intercomCall" />
    <router-view />
    
  </div>

    <div v-if="showError" @click="dismissError"  class="c-error" id="errorDiv">
        {{errorMsg}}
    </div>
</template>

<script>
import NavMenu from './homeComponents/NavMenu.vue'
import AnswerPage from './homeComponents/Answer.vue'
import DisplayTime from './homeComponents/DisplayTime.vue'
import BaseConnection from './homeComponents/BaseConnection.vue'
import CallPage from './homeComponents/CallPage.vue'
import { io } from "socket.io-client";
import { ref } from "vue";
import { useCookies } from "vue3-cookies";
import moment from 'moment';
import { uuid } from 'vue-uuid'
import {useDateFormat, useNow} from "@vueuse/core";
//const io_connection = io('https://socket.cambdoorbell.duckdns.org',{
//  cert: process.env.VUE_APP_SSL_CERT,
//  key: process.env.VUE_APP_SSL_KEY,
//  path: '/socket',
//  reconnection: true,
//  transport: ['websocket', 'polling'],
//  reconnectionAttempts: 5,
//})
const password = 'x';
const clientId = uuid.v4();
const io_connection = io('https://socket.cambdoorbell.duckdns.org',{
    auth: {
        clientId,password
    }
})

//const io_connection = io("https://socket.cambdoorbell.duckdns.org");

let localStream; //a var to hold the local video stream
let remoteStream; //a var to hold the remote video stream
let peerConnection; //the peerConnection that the two clients use to talk
let didIOffer = false;
let peerConfiguration = {
    iceServers:[
        {
            urls:[
              'stun:stun.l.google.com:19302',
              'stun:stun1.l.google.com:19302'
            ]
        }
    ]
}


const HEART_BEAT = 2000;
const connected = ref(true);
const TIME_SLICE = 5000;
var startIntercomHandler;
var sendClientAudioData;
var hangUpHandler;

const intercomCallConst = async e=>{
    await fetchUserMedia();

    //peerConnection is all set with our STUN servers sent over
    await createPeerConnection();

    //create offer time!
    try{
        console.log("Creating offer...")
        const offer = await peerConnection.createOffer();
        console.log(offer);
        peerConnection.setLocalDescription(offer);
        didIOffer = true;
        io_connection.emit('newOffer',offer); //send offer to signalingServer
    }catch(err){
        console.log(err)
    }
}
const fetchUserMedia = ()=>{
    return new Promise(async(resolve, reject)=>{
        try{
            console.log('getting user media')
            const stream = await navigator.mediaDevices.getUserMedia({
               // video: true,
               audio: true,
            });
            localStream = stream;    
            resolve();    
        }catch(err){
            console.log(err);
            reject()
        }
    })
}
const createPeerConnection = (offerObj)=>{
    return new Promise(async(resolve, reject)=>{
        //RTCPeerConnection is the thing that creates the connection
        //we can pass a config object, and that config object can contain stun servers
        //which will fetch us ICE candidates
        peerConnection = await new RTCPeerConnection(peerConfiguration)
        remoteStream = new MediaStream()
        const remoteVideoEl = document.querySelector('#remote-video');
        remoteVideoEl.srcObject = remoteStream;


        localStream.getTracks().forEach(track=>{
            //add localtracks so that they can be sent once the connection is established
            peerConnection.addTrack(track,localStream);
        })

        peerConnection.addEventListener("signalingstatechange", (event) => {
            console.log(event);
            console.log(peerConnection.signalingState)
        });

        peerConnection.addEventListener('icecandidate',e=>{
            console.log('........Ice candidate found!......')
            console.log(e)
            if(e.candidate){
                io_connection.emit('sendIceCandidateToSignalingServer',{
                    iceCandidate: e.candidate,
                    iceClientId: clientId,
                    didIOffer,
                })    
            }
        })
        
        peerConnection.addEventListener('track',e=>{
            console.log("Got a track from the other peer!! How excting")
            console.log(e)
            e.streams[0].getTracks().forEach(track=>{
                remoteStream.addTrack(track,remoteStream);
                console.log("Here's an exciting moment... fingers cross")
            })
        })

        if(offerObj){
            //this won't be set when called from call();
            //will be set when we call from answerOffer()
            // console.log(peerConnection.signalingState) //should be stable because no setDesc has been run yet
            await peerConnection.setRemoteDescription(offerObj.offer)
            // console.log(peerConnection.signalingState) //should be have-remote-offer, because client2 has setRemoteDesc on the offer
        }
        resolve();
    })
}
export default {
  name: 'Home',
  components: {
    AnswerPage,
    NavMenu,
    DisplayTime,
    BaseConnection,
    CallPage
  },
  setup() {
    const { cookies } = useCookies();
    return { cookies };
  },
  mounted() {
    
    console.log('Home.vue has mounted - process.env:')
   // console.log(process.env.VUE_APP_SSL_KEY)
   // console.log(process.env.VUE_APP_SSL_CERT)
   // console.log(process.env.VUE_APP_ROOT_URL)
    let my_cookie_user = this.cookies.get("currentUsesr");
    if(!this.beatInterval){
       this.beatInterval = setInterval(()=> {
          let now = new Date()
          let timeDiff = moment.duration(Date.parse(this.nextBeat)- now)
          console.log("current time: "+ useDateFormat(useNow(), "HH:mm:ss").value+ ", beat timeDiff: "+ timeDiff)
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
    this.dataClientId = clientId;
    //uuid.v4();  
    io_connection.on('connect', (socket) => {
      console.log('App.vue connected');
     
     // this.con = true;      
    })
    io_connection.on('messageListMsg', (message_uuid, message_list,  mp3_message_to_browser, user_generator, newIntercomClientId) => {
          this.nextBeat = moment().add(2*HEART_BEAT, 'milliseconds');
          
          if(this.intercomClientId != newIntercomClientId) {
             this.intercomClientId = newIntercomClientId;
             console.log('client id is: '+ clientId)
             console.log('intercom client id is: '+ this.intercomClientId)
          }
          if(this.current_message_uuid != message_uuid) {
             console.log('received_message list, uuid = ' + message_uuid);
             console.log('current_message_uuid = ' + this.current_message_uuid);
             console.log('mp3_message_to_browser = ' + mp3_message_to_browser);
             this.current_message_uuid = message_uuid;
             this.doormessages = message_list;
             this.mp3Played = false;
             if ( message_uuid == 0) {
                if(this.intercomRecording) {
                   this.intercomRecording = false;
                   hangUpHandler();
                }
             } 
             console.log("user generator is "+user_generator + ", and current UserID is " +  this.currentUserId);
             if(user_generator != this.currentUserId && message_uuid!=0) {
               let url = "https://assets.cambdoorbell.duckdns.org/assets/"+mp3_message_to_browser;
               console.log("Try to play the mp3: "+ url)
               if(this.soundAlertStatus && mp3_message_to_browser.length > 0 && this.mp3Played == false) {
                 var audioElement = new Audio(url);
                 audioElement.playbackRate=1.5;
                 audioElement.play();
                 this.mp3Played = true
               } else {
                 if(this.mp3Played == false) {
                      console.log("unable to play " + mp3_message_to_browser +". this.soundAlertStatus = " + this.soundAlertStatus);
                 } else {
                   console.log("File " + mp3_message_to_browser + " has already been played");
                 }
                  
               }
             }
   
          }
    })
    io_connection.on('heart_beat', () => {
//       this.nextBeat = moment().add(2*HEART_BEAT, 'milliseconds');
    })
    io_connection.on('doorbell_idle', () => {
          console.log('doorbell idle');
          this.doormessages = [];
          if(this.intercomRecording) {
             this.intercomRecording = false;
             hangUpHandler();
          }
    })
    io_connection.on('disconnect', () => {
      console.log('App.vue disconnected');
      this.con = false;
    })
    io_connection.on('sendOffer', offer=>{
      console.log('received an offer')
      this.serverOffer = offer;
    }
    if (navigator.mediaDevices.getUserMedia) {
       this.intercomPossible = true;
       console.log("The mediaDevices.getUserMedia() method is supported.");
      // this.displayError("The mediaDevices.getUserMedia() method is supported.");
       const constraints = { audio: true };
       let chunks = [];
       let onSuccess = function (stream) {
         const options = {mimeType:  'audio/webm;'};
         const mediaRecorder = new MediaRecorder(stream, options);
         startIntercomHandler = function () {
           mediaRecorder.start(TIME_SLICE);
           console.log("Recorder started.");
         }
         hangUpHandler = function () {
           mediaRecorder.stop();
           console.log("Recorder stopped.");  
         }
         mediaRecorder.ondataavailable = function (e) {
           console.log("MediaRecorder has data: "+ e);
           sendClientAudioData(e.data);
         }

         //this.mediaRecorder.ondataavailable = function (e) {
         //  console.log("We have data! "+e);
         //};  
       }
       let onError = function (err) {
         console.log("The following error occured: " + err);
       };
       navigator.mediaDevices.getUserMedia(constraints).then(onSuccess, onError);
    } else {
       this.intercomPossible = false;
       //console.log("The mediaDevices.getUserMedia() method is NOT supported.");
       this.displayError("The mediaDevices.getUserMedia() method is NOT supported.");
    }
    sendClientAudioData = function (data) {
      console.log("Sending client audio data");
      io_connection.emit('webClientAudioData', data);
    }
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
      intercomClientId: 0,
      errorMsg: '',
      showError: false,
      dataClientId: -1,
      intercomPossible: false,
      intercomRecording: false,
      mp3Played: false,
      serverOffer: null
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
    dismissError() {
      this.showError = false;
    },
    finish(interval) {
      console.log("App Finish id: " + interval)
      clearInterval(interval);

    },
    answered() {
      console.log("Answered clicked by "+ this.currentUserName);
      io_connection.emit('answered', this.currentUserId) 

    },
//    sendClientAudioData(data) {
//      console.log("Sending client audio data from clientId " +this.clientId);
//      this.io_connection.emit('webClientAudioData', this.clientId, data);
//    },
    displayError(errorMsg) {
      this.showError = true;
      this.errorMsg = errorMsg;
    },
    intercomCall() {
      console.log("Initiating Intercom Call")
      intercomCallConst()
    },

    startIntercom(client_Id) {

      console.log("startIntercom called with clientId: "+ client_Id)
      io_connection.emit('updateIntercomClientId',client_Id, this.currentUserId );
      if(!this.intercomRecording) {
         startIntercomHandler();
      }

      this.intercomRecording = true;
    },
    hangUp() {
     io_connection.emit('updateIntercomClientId',0, this.currentUserId);
     if(this.intercomRecording) {
       hangUpHandler();
     }
     this.intercomRecording  = false;
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
.c-error {
    background-color: #ffcccc; /* Light red color for the centered div */
    width: 50%; /* One-fifth of the viewport width */
    height: 50vh; /* One-fifth of the viewport height */
    position: absolute;
    top: 50%;
    left: 50%;

    display: flex;
    justify-content: center; /* Horizontally center the content */
    align-items: center; /* Vertically center the content */

    transform: translate(-50%, -50%);
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    cursor: pointer;
}

</style>
