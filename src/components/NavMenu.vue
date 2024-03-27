<template>
  <div class="c-topright d-flex">
    <h6 v-show="showUser" class="p-3">{{ currentUser }}</h6>
    <div class="c-item m-0">
      <nav class="navbar bg-light">
        <div class="container-fluid">

          <button @click="toggleUser" class="navbar-toggler ms-auto" type="button" data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
            aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div v-if="!finished" class="collapse.show navbar-collapse" id="navbarSupportedContent">
            <ul  class="list-group">

              <li v-for="user in this.users" :key="user.id" :class="{ active: user === currentUser }"
                class="list-group-item" @click="updateUser(user)">{{ user }}</li>
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
  props: ['users', 'currentUser', 'emitter'],
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
        clearInterval(this.interval)
        this.interval = setInterval(() => {
          this.now = new Date();
        }, 1000);
      
      this.until = moment().add(5, 'seconds');
      console.log("Set interval id is "+this.interval)
    },
    updateUser(newUserName) {
      console.log(newUserName);
      this.$emit('updateUser', newUserName);
    }

  }

}
</script>

<style>
.c-item {

  border: 1px solid #333;
  background-color: rgb(176, 190, 136);

}

.c-topright {
  position: absolute;
  top: 0px;
  right: 0px;
}
</style>