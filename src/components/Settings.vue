<template>

  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>
      Specify the role for each button. Button 1 is the top button on the doorbell, and button 10 is the bottom
      button.The 'Request Msg' is the message displayed on the receivers once the button
      is pressed. The 'Wait Msg' is the message played to the visitor once the button is pressed. The 'Reply Msg' is the
      message played to the visitor once someone has registered their intention to answer the door. The
      'Response Msg' is the message displayed on all the receivers once someone has registered their intention to
      answer the door. The 'Intercom Msg' is the message displayed on the receivers when someone has started an intercom session. The 'No Answer Msg' is the message played to the visitor when noone has  registered their intention to respond to the call after 30 second or so.
    </p>
    <div class="d-flex justify-content-center c-formcontainer">
      <div class="d-flex justify-content-center c-wide">
        <div class="p-2 flex-grow-1 bd-highlight c-label">Button</div>
        <div class="p-2 flex-grow-1 bd-highlight c-label">Name</div>
        <div class="p-2 flex-grow-1 bd-highlight c-label">Request Msg</div>
        <div class="p-2 flex-grow-1 bd-highlight c-label">Wait Msg</div>
        <div class="p-2 flex-grow-1 bd-highlight c-label">Reply Msg</div>
        <div class="p-2 flex-grow-1 bd-highlight c-label">Response Msg</div>
        <div class="p-2 flex-grow-1 bd-highlight c-label">Intercom Msg</div>
        <div class="p-2 flex-grow-1 bd-highlight c-label">No Answer Msg</div>

        <div style="display: none;" class="p-2 flex-grow-1 bd-highlight c-label">Phone</div>
        <div style="display: none;" class="p-2 flex-grow-1 bd-highlight c-label">Phone No.</div>
        <div class="p-2 flex-grow-1 bd-highlight c-label"></div>
      </div>
    </div>
    <div class="d-flex justify-content-center c-formcontainer">
      <div>
        <div v-for="setting in dbSettings" :key="setting.id" class="input-group mb-3">

           <form action="#" class="c-wide">
            <div class="d-flex">
          
            <span class="input-group-text flex-grow-1 c-field">{{setting.id}}</span>
            
            <textarea  :id="nameId(setting.id)" class="form-control flex-grow-1 c-field" aria-label="With textarea">{{setting.name}}</textarea>
           
            <textarea :id="RequestMsgId(setting.id)" class="form-control flex-grow-1 c-field" aria-label="With textarea">{{setting.RequestMsg}}</textarea>
            
            <textarea :id="WaitMsgId(setting.id)" class="form-control flex-grow-1 c-field" aria-label="With textarea">{{setting.WaitMsg}}</textarea>
            
            <textarea :id="ReplyMsgId(setting.id)" class="form-control flex-grow-1 c-field" aria-label="With textarea">{{setting.ReplyMsg}}</textarea>

            <textarea :id="ResponseMsgId(setting.id)" class="form-control flex-grow-1 c-field" aria-label="With textarea">{{setting.ResponseMsg}}</textarea>

            <textarea :id="IntercomMsgId(setting.id)" class="form-control flex-grow-1 c-field" aria-label="With textarea">{{setting.IntercomMsg}}</textarea>
            <textarea :id="NoAnswerMsgId(setting.id)" class="form-control flex-grow-1 c-field" aria-label="With textarea">{{setting.NoAnswerMsg}}</textarea>

            <div style="display: none;"> 
            <div  v-if="setting.Phone"  class="flex-grow-1 c-field c-check" > 
            <input  class="form-check-input flex-grow-1 c-field" checked type="checkbox" value="" :id="PhoneId(setting.id)">            
            </div>
            <div v-else  class="flex-grow-1 c-field c-check" > 
            <input  class="form-check-input flex-grow-1 c-field" type="checkbox" value="" :id="PhoneId(setting.id)">            
            </div>
            <textarea :id="PhoneNumberId(setting.id)" class="form-control flex-grow-1 c-field" aria-label="With textarea">{{setting.PhoneNumber}}</textarea>           
            </div>
            <button type="button" class="btn btn-primary flex-grow-1 c-field" v-on:click="updateSettings(setting.id)">Update</button>
            </div>
          </form>
        
        
      </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { io } from "socket.io-client";
import { uuid } from 'vue-uuid'
const settingsId = uuid.v4(); 
const userName = settingsId;
const password = 'x';
const socket = io("https://socket.cambdoorbell.duckdns.org", {    
    auth: {
        userName,password
    }
});

export default {
  name: 'Settings',
  props: {
    msg: String
  },
  methods: {
    nameId(id) {      
      return "name"+id;
    },
    RequestMsgId(id) {      
      return "RequestMsg"+id;
    },
    WaitMsgId(id) {      
      return "WaitMsg"+id;
    },
    ReplyMsgId(id) {      
      return "ReplyMsg"+id;
    },
    ResponseMsgId(id) {      
      return "ResponseMsg"+id;
    },
    IntercomMsgId(id) {
      return "IntercomMsg"+id;
    },
    NoAnswerMsgId(id) {
      return "NoAnswerMsg"+id;
    },    
    PhoneId(id) {      
      return "Phone"+id;
    },     
    PhoneNumberId(id) {      
      return "PhoneNumber"+id;
    },        
    async updateSettings(id) 
    {
      fetch('https://json.cambdoorbell.duckdns.org/settings/'+id).then(res => res.json()).then(
         data => {
          
           const newData = {
             name: document.getElementById("name"+id).value,
             RequestMsg: document.getElementById("RequestMsg"+id).value,
             WaitMsg: document.getElementById("WaitMsg"+id).value,
             ReplyMsg: document.getElementById("ReplyMsg"+id).value,
             ResponseMsg: document.getElementById("ResponseMsg"+id).value,
             IntercomMsg: document.getElementById("IntercomMsg"+id).value,
             NoAnswerMsg: document.getElementById("NoAnswerMsg"+id).value,
             Phone: document.getElementById("Phone"+id).checked,
             PhoneNumber: document.getElementById("PhoneNumber"+id).value        
           }

           const oldData = {
             name: data.name,
             RequestMsg: data.RequestMsg,
             WaitMsg: data.WaitMsg,
             ReplyMsg: data.ReplyMsg,
             ResponseMsg: data.ResponseMsg,
             IntercomMsg: data.IntercomMsg,
             NoAnswerMsg: data.NoAnswerMsg
           }
           const newJSONData = JSON.stringify(newData);
           const oldJSONData = JSON.stringify(oldData);
           console.log('About to call updateSettings: ' + newJSONData);
           socket.emit("updateSettings", id,  newJSONData, oldJSONData)
      }).catch(err => console.log(err.message))
      this.dbSettings.name =  document.getElementById("name"+id).value;
      this.dbSettings.RequestMsg =  document.getElementById("RequestMsg"+id).value; 
      this.dbSettings.WaitMsg =  document.getElementById("WaitMsg"+id).value;
      this.dbSettings.ReplyMsg =  document.getElementById("ReplyMsg"+id).value;
      this.dbSettings.ResponseMsg =  document.getElementById("ResponseMsg"+id).value;
      this.dbSettings.IntercomMsg =  document.getElementById("IntercomMsg"+id).value;
      this.dbSettings.NoAnswerMsg =  document.getElementById("NoAnswerMsg"+id).value;
      this.dbSettings.Phone =  document.getElementById("Phone"+id).value;
      this.dbSettings.PhoneNumber =  document.getElementById("PhoneNumber"+id).value;
 
    }
  },
  data () {
    return {
      dbSettings: []
    }
  },
  mounted() {
    fetch('https://json.cambdoorbell.duckdns.org/settings').then(res => res.json()).then(data => this.dbSettings = data ).catch(err => console.log(err.message))
    
    socket.on('connect', () => {
      console.log('Setting.vue connected');
      
      // const li = document.createElement('li')
      // li.textContent = "connected"
      // document.querySelector('ul').appendChild(li)
    })
    socket.on('disconnect', () => {
      console.log('Setting.vue disconnected');
      
      // const li = document.createElement('li')
      // li.textContent = "disconnected"
      // document.querySelector('ul').appendChild(li)
    })


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
.c-wide {
  width:95vw
}
.c-formcontainer {
  width:100vw
}

.c-label{
  background-color: rgb(202, 202, 249);
  border: 1px solid #333;
  flex-basis: 0;
}
.c-field {
  flex-basis: 0;
}
.c-check {

  border: 1px solid #dee2e6;
}
</style>
