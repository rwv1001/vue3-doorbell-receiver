<template>
   <div class="d-none d-lg-block"> 
      <Icon v-if="connected && answering" icon="ph:wifi-high-bold" class="big-icon c-topleft" />
      <Icon v-else-if="!connected && answering" icon="ph:wifi-slash-bold" class="big-icon c-topleft" />
      <Icon v-else-if="connected && !answering" icon="ph:wifi-high-bold" class="big-icon c-topleft" />
      <Icon v-else icon="ph:wifi-slash-bold" class="big-icon c-topleft" />
      <div v-if="!intercomRecording  && !isSafari()" class="c-bottomright1 c-clickable" >
       <Icon v-if="soundAlert && answering" icon="fluent:speaker-2-20-filled" class="big-icon c-bottomright1 c-clickable c-answering" @click="toggleSoundAlertHandler" />
       <Icon v-else-if="!soundAlert && answering" icon="fluent:speaker-off-20-filled" class="big-icon c-answering" @click="toggleSoundAlertHandler" />
       <Icon v-else-if="soundAlert && !answering" icon="fluent:speaker-2-20-filled" class="big-icon c-bottomright1 c-clickable" @click="toggleSoundAlertHandler" />
       <Icon v-else icon="fluent:speaker-off-20-filled" class="big-icon" @click="toggleSoundAlertHandler" />
       </div>
    </div>
   <div class="d-lg-none">
      <Icon v-if="connected && answering" icon="ph:wifi-high-bold" class="small-icon c-topleft" />
      <Icon v-else-if="!connected && answering" icon="ph:wifi-slash-bold" class="small-icon c-topleft" />
      <Icon v-else-if="connected && !answering" icon="ph:wifi-high-bold" class="small-icon c-topleft" />
      <Icon v-else icon="ph:wifi-slash-bold" class="small-icon c-topleft" />
      <div v-if="!intercomRecording  && !isSafari()" class="c-bottomright1 c-clickable" >
       <Icon v-if="soundAlert && answering" icon="fluent:speaker-2-20-filled" class="small-icon c-bottomright1 c-clickable c-answering" @click="toggleSoundAlertHandler" />
       <Icon v-else-if="!soundAlert && answering" icon="fluent:speaker-off-20-filled" class="small-icon c-answering" @click="toggleSoundAlertHandler" />
       <Icon v-else-if="soundAlert && !answering" icon="fluent:speaker-2-20-filled" class="small-icon c-bottomright1 c-clickable" @click="toggleSoundAlertHandler" />
       <Icon v-else icon="fluent:speaker-off-20-filled" class="small-icon" @click="toggleSoundAlertHandler" />
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

.c-bottomright1 {
  position: fixed;
  bottom: 0px;
  right: 0px;
  z-index: 1000;
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
