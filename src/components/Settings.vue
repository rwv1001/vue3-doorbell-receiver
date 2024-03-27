<template>

  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>
      Specify the role for each button. Button 1 is the top button on the doorbell, and button 10 is the bottom
      button.The 'Request Msg' is the message displayed on the receivers once the button
      is pressed. The 'Wait Msg' is the message played to the visitor once the button is pressed. The 'Reply Msg' is the
      message played to the visitor once someone has registered their intention to answer the door. The
      'Response Msg' is the message displayed on all the receivers once someone has registered their intention to
      answer the door.
    </p>
    <div class="d-flex justify-content-center c-formcontainer">
      <div class="d-flex justify-content-center c-wide">
        <div class="p-2 flex-grow-1 bd-highlight c-label">Button</div>
        <div class="p-2 flex-grow-1 bd-highlight c-label">Name</div>
        <div class="p-2 flex-grow-1 bd-highlight c-label">Request Msg</div>
        <div class="p-2 flex-grow-1 bd-highlight c-label">Wait Msg</div>
        <div class="p-2 flex-grow-1 bd-highlight c-label">Reply Msg</div>
        <div class="p-2 flex-grow-1 bd-highlight c-label">Response Msg</div>
        <div class="p-2 flex-grow-1 bd-highlight c-label">Phone</div>
        <div class="p-2 flex-grow-1 bd-highlight c-label">Phone No.</div>
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

            <div  v-if="setting.Phone"  class="flex-grow-1 c-field c-check" > 
            <input  class="form-check-input flex-grow-1 c-field" checked type="checkbox" value="" :id="PhoneId(setting.id)">            
            </div>
            <div v-else  class="flex-grow-1 c-field c-check" > 
            <input  class="form-check-input flex-grow-1 c-field" type="checkbox" value="" :id="PhoneId(setting.id)">            
            </div>
            <textarea :id="PhoneNumberId(setting.id)" class="form-control flex-grow-1 c-field" aria-label="With textarea">{{setting.PhoneNumber}}</textarea>           

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
    PhoneId(id) {      
      return "Phone"+id;
    },     
    PhoneNumberId(id) {      
      return "PhoneNumber"+id;
    },        
    async updateSettings(id) 
    {
      let newname = document.getElementById("name"+id).value;
      let newRequestMsg = document.getElementById("RequestMsg"+id).value;
      let newWaitMsg = document.getElementById("WaitMsg"+id).value;
      let newReplyMsg = document.getElementById("ReplyMsg"+id).value;
      let newResponseMsg = document.getElementById("ResponseMsg"+id).value;
      let newPhone = document.getElementById("Phone"+id).checked;
      let newPhoneNumber = document.getElementById("PhoneNumber"+id).value;
      
      const result = await axios.put("http://192.168.1.47:3000/settings/"+id,{
        name:newname,
        RequestMsg:newRequestMsg,
        WaitMsg:newWaitMsg,
        ReplyMsg:newReplyMsg, 
        ResponseMsg:newResponseMsg,
        Phone:newPhone,   
        PhoneNumber:newPhoneNumber
      });
      console.log("id: "+id+", newRequestMsg: "+ newRequestMsg + ", result: " + result.status + " result-text: " + result.statusText )
    }
  },
  data () {
    return {
      dbSettings: []
    }
  },
  mounted() {
    fetch('http://192.168.1.47:3000/settings').then(res => res.json()).then(data => this.dbSettings = data ).catch(err => console.log(err.message))
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
