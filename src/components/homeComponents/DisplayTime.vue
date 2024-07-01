<template>
    <div class="d-none d-sm-block">
    <div class="c-date d-flex justify-content-center fw-bold">
      <div class="align-self-center c-prevent-select"> 
        <h2>{{currentDate}}</h2> 
      </div>
    </div>
    </div>
    <div class="d-block d-sm-none">
    <div class="c-date-small d-flex justify-content-center fw-bold">
      <div class="align-self-center c-prevent-select">
        <h5 class="d-block d-sm-none">{{currentDate}}</h5>
      </div>
    </div>
    </div>
    <div class="c-time flex-fill d-flex justify-content-center ">  
      <h1 class="align-self-center m-0 display-1 fw-bold c-prevent-select">{{currentTime}}</h1>
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
}
.c-time{
  
  width:100vw;
  border: 1px solid #333;
  background-color:rgb(255, 255, 255);
}
.c-date-small{
  height: 12vh;
  width:100vw;
  border: 1px 0px 0px 0px solid #333;
  background-color:rgb(255, 255, 255);
}


.c-date{
  height: 20vh;
  width:100vw;
  border: 1px 0px 0px 0px solid #333;
  background-color:rgb(255, 255, 255);
}

.c-date-small{
  height: 10vh;
  width:100vw;
  border: 1px 0px 0px 0px solid #333;
  background-color:rgb(255, 255, 255);
}
.c-prevent-select {
  -webkit-user-select: none; /* Safari */
  -ms-user-select: none; /* IE 10 and IE 11 */
  user-select: none; /* Standard syntax */
}

</style>
