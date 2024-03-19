<template>
  <NavMenu :currentUser="currentUser" :users="users" @updateUser="updateUser" "/>
  <AnswerPage v-if="justRang"  />
  <DisplayTime />
</template>

<script>
import NavMenu from './components/NavMenu.vue'
import AnswerPage from './components/Answer.vue'
import DisplayTime from './components/DisplayTime.vue'



export default {
  name: 'App',
  components: {
    AnswerPage, 
    NavMenu,
    DisplayTime
  },
  data() {
    return {
      justRang: false,
      currentUser: 'Fr Robert',
      users: [  'Generalt','Fr Robert','Fr Greg','Fr Albert' ]
    }
  },
  methods: {
    updateUser(newUserName) {
      console.log('Update aaaaa' )
      this.currentUser = newUserName;     
    }

  }
}
</script>

<style >
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
body {
  overflow: hidden; /* Hide scrollbars */
}

</style>
