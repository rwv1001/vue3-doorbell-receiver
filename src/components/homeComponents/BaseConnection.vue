<template>
   <div class="d-none d-lg-block"> 
      <span v-if="connected && answering"  class="big-icon c-topleft c-connected-big" />
      <span v-else-if="!connected && answering"  class="big-icon c-topleft c-disconnected-big" />
      <span v-else-if="connected && !answering"  class="big-icon c-topleft c-connected-big" />
      <span v-else  class="big-icon c-topleft c-disconnected-big" />
      <div v-if="!intercomRecording  && !isSafari()" class="c-bottomright1 c-clickable" >
       <span v-if="soundAlert && answering"  class="big-icon c-clickable c-answering c-unmuted-big-invert" @click="toggleSoundAlertHandler" />
       <span v-else-if="!soundAlert && answering" class="big-icon c-answering c-muted-big-invert" @click="toggleSoundAlertHandler" />
       <span v-else-if="soundAlert && !answering" class="big-icon c-clickable c-unmuted-big" @click="toggleSoundAlertHandler" />
       <span v-else class="big-icon c-muted-big" @click="toggleSoundAlertHandler" />
       </div>
    </div>
   <div class="d-lg-none">
      <span v-if="connected && answering"  class="small-icon c-topleft c-connected-small" />
      <span v-else-if="!connected && answering"  class="small-icon c-topleft c-disconnected-small" />
      <span v-else-if="connected && !answering"  class="small-icon c-topleft c-connected-small"  />
      <span v-else  class="small-icon c-topleft c-disconnected-small" />
      <div v-if="!intercomRecording  && !isSafari()" class="c-bottomright1 c-clickable" >
       <span v-if="soundAlert && answering"  class="small-icon c-clickable c-answering c-unmuted-small-invert" @click="toggleSoundAlertHandler" />
       <span v-else-if="!soundAlert && answering"  class="small-icon c-answering c-muted-small-invert" @click="toggleSoundAlertHandler" />
       <span v-else-if="soundAlert && !answering"  class="small-icon c-clickable c-unmuted-small" @click="toggleSoundAlertHandler" />
       <span v-else  class="small-icon c-muted-small" @click="toggleSoundAlertHandler" />
       </div>
    </div>


</template>
  
  <script>
  import { Icon } from '@iconify/vue';
  export default { 
    props: ['connected','answering','soundAlert','intercomRecording'], 
    emits: ["toggleSoundAlert"],  
    components: {
      Icon,
    },
    name: 'BaseConnection',
    mounted() {

    },
    data() {
      return {  
      }
   
    },
    methods: {
      isSafari() {
        return  /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
      },
      toggleSoundAlertHandler() {
        this.$emit('toggleSoundAlert');
      }
    }

  }
  </script>
  
  <style>
.c-topleft {
  position: absolute;
  top: 0px;
  left: 0px;
}

.c-connected-small {
  display: inline-block;
  width: 70px;
  height: 70px;
   /* Add background image */
  background-repeat: no-repeat;
  background-size: 100% 100%;
  margin:0;
  background-image: url( 'https://assets.cambdoorbell.duckdns.org/assets/wifi-high-bold-svgrepo-com.svg' );
}
.c-connected-big {
  display: inline-block;
  width: 100px;
  height: 100px;
   /* Add background image */
  background-repeat: no-repeat;
  background-size: 100% 100%;
  margin:0;
  background-image: url( 'https://assets.cambdoorbell.duckdns.org/assets/wifi-high-bold-svgrepo-com.svg' );
}
.c-disconnected-small {
  display: inline-block;
  width: 70px;
  height: 70px;
   /* Add background image */
  background-repeat: no-repeat;
  background-size: 100% 100%;
  margin:0;
  background-image: url( 'https://assets.cambdoorbell.duckdns.org/assets/wifi-slash-bold-svgrepo-com.svg' );
}
.c-disconnected-big {
  display: inline-block;
  width: 100px;
  height: 100px;
   /* Add background image */
  background-repeat: no-repeat;
  background-size: 100% 100%;
  margin:0;
  background-image: url( 'https://assets.cambdoorbell.duckdns.org/assets/wifi-slash-bold-svgrepo-com.svg' );
}
.c-unmuted-small {
  display: inline-block;
  width: 70px;
  height: 70px;
   /* Add background image */
  background-repeat: no-repeat;
  background-size: 100% 100%;
  margin:0;
  position: fixed;
  bottom: 0px;
  right: 0px;
  z-index: 1000;
  background-image: url( 'https://assets.cambdoorbell.duckdns.org/assets/fluent--speaker-2-20-filled.svg' );
}
.c-unmuted-big {
  display: inline-block;
  width: 100px;
  height: 100px;
   /* Add background image */
  background-repeat: no-repeat;
  background-size: 100% 100%;
  margin:0;
  position: fixed;
  bottom: 0px;
  right: 0px;
  z-index: 1000;
  background-image: url( 'https://assets.cambdoorbell.duckdns.org/assets/fluent--speaker-2-20-filled.svg' );
}
.c-muted-small {
  display: inline-block;
  width: 70px;
  height: 70px;
   /* Add background image */
  background-repeat: no-repeat;
  background-size: 100% 100%;
  margin:0;
  position: fixed;
  bottom: 0px;
  right: 0px;
  z-index: 1000;
  background-image: url( 'https://assets.cambdoorbell.duckdns.org/assets/fluent--speaker-off-20-filled.svg' );
}
.c-muted-big {
  display: inline-block;
  width: 100px;
  height: 100px;
   /* Add background image */
  background-repeat: no-repeat;
  background-size: 100% 100%;
  margin:0;
  position: fixed;
  bottom: 0px;
  right: 0px;
  z-index: 1000;

  background-image: url( 'https://assets.cambdoorbell.duckdns.org/assets/fluent--speaker-off-20-filled.svg' );
}
.c-unmuted-small-invert {
  display: inline-block;
  width: 70px;
  height: 70px;
   /* Add background image */
  background-repeat: no-repeat;
  background-size: 100% 100%;
  margin:0;
  position: fixed;
  bottom: 0px;
  right: 0px;
  z-index: 1000;
  filter: invert(1);
  background-image: url( 'https://assets.cambdoorbell.duckdns.org/assets/fluent--speaker-2-20-filled.svg' );
}
.c-unmuted-big-invert {
  display: inline-block;
  width: 100px;
  height: 100px;
   /* Add background image */
  background-repeat: no-repeat;
  background-size: 100% 100%;
  margin:0;
  position: fixed;
  bottom: 0px;
  right: 0px;
  z-index: 1000;
  filter: invert(1);
  background-image: url( 'https://assets.cambdoorbell.duckdns.org/assets/fluent--speaker-2-20-filled.svg' );
}
.c-muted-small-invert {
  display: inline-block;
  width: 70px;
  height: 70px;
   /* Add background image */
  background-repeat: no-repeat;
  background-size: 100% 100%;
  margin:0;
  position: fixed;
  bottom: 0px;
  right: 0px;
  z-index: 1000;
  filter: invert(1);
  background-image: url( 'https://assets.cambdoorbell.duckdns.org/assets/fluent--speaker-off-20-filled.svg' );
}
.c-muted-big-invert {
  display: inline-block;
  width: 100px;
  height: 100px;
   /* Add background image */
  background-repeat: no-repeat;
  background-size: 100% 100%;
  margin:0;
  position: fixed;
  bottom: 0px;
  right: 0px;
  z-index: 1000;
  filter: invert(1);

  background-image: url( 'https://assets.cambdoorbell.duckdns.org/assets/fluent--speaker-off-20-filled.svg' );
}


.c-bottomright1 {
  position: fixed;
  bottom: 0px;
  right: 0px;
  z-index: 1000;
  padding: 0;
  margin: 0;
}

svg {
   font-size: 24px;
   line-height: 1em;
}
.small-icon {
   font-size: 70px;
}

.big-icon {
   font-size: 100px;
}
.c-clickable:hover {
  cursor: pointer;
}

.c-answering {
   color: white;
}
  </style>
