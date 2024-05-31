
<template>
  <div id="home" class="d-flex flex-column c-fullheight border border-dark border-top-1 border-bot-0">
  <div class="row justify-content-center">
    <div class="col-auto  flex-fill"></div>
    <div class="col-auto bg-lightgrey border border-3 border-top-0 border-dark rounded-bottom pt-1 pb-0 text-center"><h6>{{currentUserName}}</h6></div>
    <div class="col-auto  flex-fill"></div>
  </div> 
    <NavMenu :currentUserId="currentUserId" :currentUserName="currentUserName" @updateUser="updateUser"
      @finish="finish" />


    <AnswerPage v-if="doormessages.length" :doormessages="doormessages" @startIntercom="startIntercom" @answered="answered" @hangUp="hangUp" :dataClientId="dataClientId" :intercomClientId="intercomClientId" :intercomPossible="intercomPossible"/>
    <BaseConnection :connected="con" :answering="doormessages.length>0" :soundAlert="soundAlertStatus" @toggleSoundAlert="toggleSoundAlert" :intercomRecording="intercomRecording"/>
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
const userName = clientId;
const io_connection = io('https://socket.cambdoorbell.duckdns.org',{
    auth: {
        userName,password
    }
})

//const io_connection = io("https://socket.cambdoorbell.duckdns.org");

let localStream; //a var to hold the local video stream
let remoteStream; //a var to hold the remote video stream
let peerConnection = null; //the peerConnection that the two clients use to talk
let didIOffer = false;
let muted = true;
let peerConfiguration = {
    iceServers:[
        {
            urls:[
               'stun:cambdoorbell.duckdns.org:3478'
              //'stun:stun.l.google.com:19302',
              //'stun:stun1.l.google.com:19302'
            ]
        }
    ]
}


const HEART_BEAT = 2000;
const connected = ref(true);
let hangingup = false;
let heartbeatcount = 0;
let sendingNewOffer = false;
const SENDING_NEW_OFFER_INTERVAL = 10000;
const  HANGUPBEATS = 5; 
const intercomCallConst = async e=>{
    didIOffer = true;
    console.log("intercomCallConst userName = " + userName) 
    await fetchUserMedia();

    //peerConnection is all set with our STUN servers sent over
    await createPeerConnection();

    //create offer time!
    try{
        console.log("Creating offer...")
        const offer = await peerConnection.createOffer();
        console.log(offer);
        peerConnection.setLocalDescription(offer);
        console.log("Sending newOffer")
        sendingNewOffer = true;
        io_connection.emit('newOffer',offer); //send offer to signalingServer
        let actionInterval = setInterval(() => {  
            if(sendingNewOffer) {
               console.log('Action NOT performed - emit newOffer');
               //io_connection.emit('newOffer',offer);
            } else {
               clearInterval(actionInterval); // Clear the interval
               console.log('Timer stopped');
            }

        }, SENDING_NEW_OFFER_INTERVAL);
    }catch(err){
        didIOffer = false;
        console.log(err)
    }
}

const answerResponseConst = async(offerObj)=>{
    //addAnswer is called in socketListeners when an answerResponse is emitted.
    //at this point, the offer and answer have been exchanged!
    //now CLIENT1 needs to set the remote
    await peerConnection.setRemoteDescription(offerObj.answer)
    console.log("answerResponseConst peerConnection:")
    console.log(peerConnection)


}

const startIntercomConst = async(offerObj)=>{
    console.log("startIntercomConst userName = " + userName)
    console.log("startIntercomConst called fetchUserMedia")
    await fetchUserMedia()
    console.log("startIntercomConst called createPeerConnection(offerObj)");
    await createPeerConnection(offerObj);
    const answer = await peerConnection.createAnswer({}); //just to make the docs happy
    console.log("startIntercomConst called await peerConnection.createAnswer({});")
    await peerConnection.setLocalDescription(answer); //this is CLIENT2, and CLIENT2 uses the answer as the localDesc
    console.log("startIntercomConst called await peerConnection.setLocalDescription(answer);")
    console.log("**** offerObj ****")
    console.log(offerObj)
    console.log("**** answer ****")
    console.log(answer)
    // console.log(peerConnection.signalingState) //should be have-local-pranswer because CLIENT2 has set its local desc to it's answer (but it won't be)
    //add the answer to the offerObj so the server knows which offer this is related to
    offerObj.answer = answer 
    //emit the answer to the signaling server, so it can emit to CLIENT1
    //expect a response from the server with the already existing ICE candidates
    console.log("EmitWithAck newAnswer")
    const offerIceCandidates = await io_connection.emitWithAck('newAnswer',offerObj)
    offerIceCandidates.forEach(c=>{
        peerConnection.addIceCandidate(c);
        console.log("======Added Ice Candidate======")
    })
    console.log(offerIceCandidates)
    console.log("startIntercomConst peerConnection:")
    console.log(peerConnection) 

}

const hangupConst = async () => {
    await peerConnection.close()
    io_connection.emit('hangupReset')
    peerConnection = null;
    hangingup = true;
}

const fetchUserMedia = ()=>{
    return new Promise(async(resolve, reject)=>{
        try{
            console.log('getting user media')
            const stream = await navigator.mediaDevices.getUserMedia({
               // video: true,
               audio: true,
            });
            console.log('Setting local Streat');
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
        if(peerConnection != null){
          peerConnection.close()
        }
        peerConnection = await new RTCPeerConnection(peerConfiguration)
        remoteStream = new MediaStream()
        const remoteVideoEl = document.querySelector('#remote-video');
        remoteVideoEl.srcObject = remoteStream;

        console.log("Let's add some tracks to local stream")
        localStream.getTracks().forEach(track=>{
            console.log("Adding a track to local stream")
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
                console.log("createPeerConnection: Emit sendIceCandidateToSignalingServer, didIOffer = " + didIOffer)
                io_connection.emit('sendIceCandidateToSignalingServer',{
                    iceCandidate: e.candidate,
                    iceUserName: userName,
                    didIOffer,
                })    
            }
        })
        
        peerConnection.addEventListener('track',e=>{
            console.log("Got a track from the other peer!! How excting")
            console.log(e)
            e.streams[0].getTracks().forEach(track=>{
                remoteStream.addTrack(track,remoteStream);
                console.log("*******************  Here's an exciting moment... fingers cross ****************************")
            })
        })

        if(offerObj){
            //this won't be set when called from call();
            //will be set when we call from answerOffer()
            // console.log(peerConnection.signalingState) //should be stable because no setDesc has been run yet
            console.log("createPeerConnection: peerConnection.setRemoteDescription(offerObj.offer)")
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
          heartbeatcount++;
          console.log("current time: "+ useDateFormat(useNow(), "HH:mm:ss").value+ ", beat timeDiff: "+ timeDiff + ", heartbeatcount = " + heartbeatcount)
          if(timeDiff < 0){
            this.con = false 
          } else {
            this.con = true;
          }
          if(heartbeatcount%HANGUPBEATS == 0 && hangingup) {
            console.log('do not emit hangup beat reset')
           // io_connection.emit('hangupReset')
          }
       }, HEART_BEAT)
    }
 //   fetch('https://json.cambdoorbell.duckdns.org/settings').then(res => res.json()).then(data =>{
 //      data.forEach((item) => {
 //         console.log("mounted wait file: "+ item.WaitMsgFile)
 //         this.pushMP3(item.NoAnswerMsgFile)
 //         this.pushMP3(item.RequestMsgFile)
 //         this.pushMP3(item.WaitMsgFile)
 //         this.pushMP3(item.ReplyMsgFile)
 //         this.pushMP3(item.ResponseMsgFile)
 //         this.pushMP3(item.IntercomMsgFile)
 //      })
//    }).catch(err => console.log(err.message))

    if(my_cookie_user != null) {
      this.currentUserName = my_cookie_user.name;
      this.currentUserId = my_cookie_user.id;
    }
    console.log("Cookie user: "+ my_cookie_user);
    this.dataClientId = clientId;
    //uuid.v4();  
    io_connection.on('connect', (socket) => {
      if(socket){
        const keys = Object.keys(socket);
        console.log("Attributes of socket:");
        keys.forEach((key) => {
           console.log(key);
        });    
        console.log('App.vue connected, socket_id = ' );
      }
     // this.con = true;      
    })
 //   io_connection.on('registerMP3Files', (files) => {
   //   console.log("handling registerMP3Files")
 //     files.forEach((fileName) => {
      // Your custom action here

   //      console.log(`Processing file in registerMP3Files handler: ${fileName}`);
     //    const url = "https://assets.cambdoorbell.duckdns.org/assets/"+fileName
   //      const audioElement = new Audio(url);
   //      audioPair = {url:url, audioObject: audioElement}
   //      this.audioPairs.push(audioPair)

     // });
    //})
    io_connection.on('intercomTimeout', ()=> {
       if(this.intercomRecording) {
          this.intercomRecording = false;
          hangupConst();
       }
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
                   hangupConst();
                }
             } 
             console.log("messageListMsg:  intercomClientId = " +  this.intercomClientId + ", intercomPossible = " + this.intercomPossible)
             console.log("user generator is "+user_generator + ", and current UserID is " +  this.currentUserId);
             if(user_generator != this.currentUserId && message_uuid!=0) {
               let url = "https://assets.cambdoorbell.duckdns.org/assets/"+mp3_message_to_browser;
               console.log("Try to play the mp3: "+ url)
               var audioPair = this.audioPairs.find(pair => pair.url === url);
               if(!audioPair && mp3_message_to_browser.length > 0) {
                 if(this.offerer) {
                  const audioElement = new Audio(url);
                  audioPair = {url:url, audioObject: audioElement}
                  this.audioPairs.push(audioPair)
                  this.soundAlertStatus = false;
                  io_connection.emit('consoleLog', "had to create audio object for " + url )
                  } else {
                    this.soundAlertStatus  = false;
                  }
               } else {
                  io_connection.emit('consoleLog', "found audio pair for  " + url )
               }

               if(this.soundAlertStatus && mp3_message_to_browser.length > 0 && this.mp3Played == false && audioPair) {
                 audioPair.audioObject.playbackRate=1.5;
                 audioPair.audioObject.volume = 1;
                 if(!this.isSafari() ){
                    audioPair.audioObject.play();
                 }
                 this.mp3Played = true
                  io_connection.emit('consoleLog', "played " + url )
               } else {
                 if(this.mp3Played == false) {
                      io_connection.emit('consoleLog', "unable to play " + mp3_message_to_browser +". this.soundAlertStatus = " + this.soundAlertStatus )
                      console.log("unable to play " + mp3_message_to_browser +". this.soundAlertStatus = " + this.soundAlertStatus);
                 } else {
                   console.log("File " + mp3_message_to_browser + " has already been played");
                    io_connection.emit('consoleLog',"File " + mp3_message_to_browser + " has already been played");
                 }
                  
               }
             }
   
          }
    })
    io_connection.on('playfile', (mp3_message_to_puppeteer) => {
       let url = "https://assets.cambdoorbell.duckdns.org/assets/"+mp3_message_to_puppeteer;
       console.log("playfile, Try to play the mp3: "+ url + ", offerer = " + this.offerer)
       if(mp3_message_to_puppeteer.length > 0 && this.offerer) {
            var audioElement = new Audio(url);
            audioElement.playbackRate=1.2;
            audioElement.play();
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
             hangupConst();
          }
    })
    io_connection.on('disconnect', () => {
      console.log('App.vue disconnected');
      //this.soundAlertStatus = false;
      this.con = false;
    })
    io_connection.on('sendOffer', offer=>{
      console.log('received an offer')
      this.intercomPossible = true;
      this.serverOffer = offer;
    })
    io_connection.on('answerResponse', offerObj=>{
      console.log('Handling answerResponse')
      console.log(offerObj)
      answerResponseConst(offerObj)
    })
    io_connection.on('receivedIceCandidateFromServer',iceCandidate=>{
      console.log('*********** Handling receivedIceCandidateFromServer ******************')
      peerConnection.addIceCandidate(iceCandidate)
      console.log(iceCandidate)
    })
    io_connection.on('resetOffer', () => {
      if(this.offerer) {
         console.log('Handling resetOffer')
         intercomCallConst() 
      } else {
        console.log('resetOffer: client is not offerer');
      } 
    })
    io_connection.on('hangupResponse', () => {
      console.log('Handling hangupResponse')
      hangingup = false;
      if(peerConnection !=null) {
        peerConnection.close()
        peerConnection = null
      }
      this.intercomRecording  = false;
    })
    io_connection.on('sendOfferAcknowledgment', () => {
      console.log('Handling sendOfferAcknowledgment')
      sendingNewOffer = false;
    })


  },
  data() {
    return {
      justRang: false,
      doormessages: [],
      current_message_uuid: 0,
      con: false,
      currentUserId: 1,
      currentUserName: 'Not Assigned',
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
      serverOffer: null,
      offerer: false,
      audioPairs: []
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
    isSafari() {
      return  /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
    },
    pushMP3(url){
       const mp3URL = "https://assets.cambdoorbell.duckdns.org/assets/"+url;
       var audioPair = this.audioPairs.find(pair => pair.url === mp3URL);
       if(!audioPair){
         const audioElement = new Audio(mp3URL);
         audioElement.volume = 0.0001;
         if(!this.isSafari() ){
           audioElement.play();
         }
         //audioElement.volume = 1;
         const audioPair = {url:mp3URL, audioObject: audioElement}
         this.audioPairs.push(audioPair)
         io_connection.emit('consoleLog', "Pushing "+  mp3URL)
       } else {
         io_connection.emit('consoleLog', "Not pushing "+  mp3URL)
       }

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
    displayError(errorMsg) {
      this.showError = true;
      this.errorMsg = errorMsg;
    },
    intercomCall() {
      console.log("Initiating Intercom Call")
      this.offerer = true;
      intercomCallConst()
    },
    startIntercom() {
      console.log("startIntercom called with clientId: "+ clientId)
      if(!this.intercomRecording && this.serverOffer){
         startIntercomConst(this.serverOffer)
         this.intercomRecording = true;
         console.log("Emitting updateIntercomClientId")
         io_connection.emit('updateIntercomClientId',clientId, this.currentUserId );
      } else {
        console.log("For some reason, we didn't start startIntercomConst")
        console.log("this.intercomRecording = " + this.intercomRecording)
        console.log("this.serverOffer = " +  this.serverOffer);
      }
    },
    hangUp() {
     io_connection.emit('updateIntercomClientId',0, this.currentUserId);
     if(this.intercomRecording) {
       hangupConst();
     }
     // this.intercomRecording  = false;
    },
    async  hangupConst() {
      await peerConnection.close()
      peerConnection = null
      io_connection.emit('hangupReset')
      
      hangingup = true;
    },
 
    toggleSoundAlert() {
      this.soundAlertStatus = !this.soundAlertStatus;
      muted = !muted;
      let silentUrl = "https://assets.cambdoorbell.duckdns.org/assets/silent.mp3";
      var audioPair = this.audioPairs.find(pair => pair.url === silentUrl);
      if(!audioPair) {
         const audioElement = new Audio("https://assets.cambdoorbell.duckdns.org/assets/silent.mp3");
         audioPair = {url:silentUrl, audioObject: audioElement}
         this.audioPairs.push(audioPair)
         io_connection.emit('consoleLog', "Silence created" )
      } else {
        io_connection.emit('consoleLog', "Silence found" )
      }

      audioPair.audioObject.playbackRate=1.5;
      if(!this.isSafari() ){
         audioPair.audioObject.play();
      }
      console.log("soundAlertStatus = " + this.soundAlertStatus);
      if(this.soundAlertStatus){
        io_connection.emit('consoleLog', "fetching json data" )
        fetch('https://json.cambdoorbell.duckdns.org/settings').then(res => res.json()).then(data =>{
           io_connection.emit('consoleLog', "Got json data" )
           data.forEach((item) => {
              io_connection.emit('consoleLog',"mounted wait file: "+ item.WaitMsgFile)
              console.log("mounted wait file: "+ item.WaitMsgFile)
              this.pushMP3(item.NoAnswerMsgFile)
              this.pushMP3(item.RequestMsgFile)
              this.pushMP3(item.WaitMsgFile)
              this.pushMP3(item.ReplyMsgFile)
              this.pushMP3(item.ResponseMsgFile)
              this.pushMP3(item.IntercomMsgFile)
           })
        }).catch(err => {
           console.log(err.message)
           io_connection.emit('consoleLog',err.message)
           })
      }
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
.bg-lightgrey {
  background-color: lightgrey;
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
