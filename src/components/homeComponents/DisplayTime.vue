<template>
  <div class="d-flex flex-column c-fullheight">
    <div class="c-date d-flex justify-content-center fw-bold">
      <h2 class="align-self-center"> {{currentDate}} </h2>
    </div>
    <div class="c-time flex-fill d-flex justify-content-center ">  
      <h1 class="align-self-center m-0 display-1 fw-bold">{{currentTime}}</h1>
    </div>
  </div>
</template>

<script>
import {useDateFormat, useNow} from "@vueuse/core";
export default {
    name: 'DisplayTime', 
    mounted() {
      this.currentDate = useDateFormat(useNow(), "ddd, D MMM,  YYYY");
      this.currentTime = useDateFormat(useNow(), "HH:mm:ss");
    },
    data() {
    return {
      currentTime: null,
      currentDate: null
    }
  },

}
</script>

<style>
.c-fullheight{
  height: 100vh;
  background-color: blue;
}
.c-time{
  
  width:100vw;
  border: 1px solid #333;
  background-color:rgb(255, 255, 255);
}
.c-date{
  height: 20vh;
  width:100vw;
  border: 1px solid #333;
  background-color:rgb(255, 255, 255);
}
</style>