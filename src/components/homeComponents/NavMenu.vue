<template>
  <div class="c-topright d-flex">
    <div class="c-item m-0">
      <nav class="navbar bg-light ">
        <div class="container-fluid">
          <button @click="toggleUser" class="d-lg-none navbar-toggler ms-auto c-navbar-toggler" type="button" data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
            aria-label="Toggle navigation">
            <span class="navbar-toggler-icon c-navbar-toggler-icon c-prevent-select"></span>
          </button>
          <button @click="toggleUser" class="d-none d-lg-block navbar-toggler ms-auto" type="button" data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
            aria-label="Toggle navigation">
            <span class="navbar-toggler-icon c-prevent-select"></span>
          </button>

          <div v-if="!finished" class="collapse.show navbar-collapse" id="navbarSupportedContent">
            <ul  class="list-group">
              <div  v-for="user in this.users" :key="user.id">  
              <li  v-if="user.name.length>0"  :class="{ active: user.name === currentUserName }"
                class="list-group-item" @click="updateUser(user.id, user.name)">{{ user.name }}</li>

              </div>    
            </ul>

          </div>
        </div>
      </nav>

    </div>
  </div>
</template>

<script>

import moment from 'moment';



export default {
  props: ['currentUserId', 'currentUserName'],
  name: 'NavMenu',
  mounted() {
    this.closeTime = (new Date()).getTime();  
    
  },
  created() {
    
  },

  data() {
    return {
      showMenu: false,
      showUser: true,
      users: [],
      now: new Date(),
      until: new Date(),
      interval: 0
    }
  },
  computed: {
    finished() {
      return this.remaining <= 0;
    },
    remaining() {
      let remaining = moment.duration(Date.parse(this.until) - this.now);
      console.log("Called remaining")
      if (remaining <= 0) {
        this.$emit('finish', this.interval);         
        console.log("Called remaining in finish state")
       
      }
      return remaining;
    }

  },
  methods: {
    toggleUser() {
      fetch('https://json.cambdoorbell.duckdns.org/settings').then(res => res.json()).then(data => this.users = data ).catch(err => console.log(err.message))
        clearInterval(this.interval)
        this.interval = setInterval(() => {
          this.now = new Date();
        }, 1000);
      
      this.until = moment().add(5, 'seconds');
      console.log("Set interval id is "+this.interval)
    },
    updateUser(newUserId, newUserName) {
      console.log(newUserId);
      this.$emit('updateUser', newUserId, newUserName);
    }

  }

}
</script>

<style>

.c-item {

  border: 1px solid #333;
  background-color: rgb(176, 190, 136);

}
.c-navbar-toggler {
  padding: 0rem; /* Adjusts the padding around the icon */
  width: 3rem; /* Adjusts the width of the button */
  height: 3rem; /* Adjusts the height of the button */
}

.c-navbar-toggler-icon {
  font-size: 0.5em; /* Adjusts the size of the icon bars */
  transform: translateY(-4px);
}


.c-topright {
  position: absolute;
  top: 0px;
  right: 0px;
}

.c-prevent-select {
  -webkit-user-select: none; /* Safari */
  -ms-user-select: none; /* IE 10 and IE 11 */
  user-select: none; /* Standard syntax */
}
</style>
