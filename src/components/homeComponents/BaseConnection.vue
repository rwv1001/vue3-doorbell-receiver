<template>
    
    <Icon v-if="connected && answering" icon="ph:wifi-high-bold" class="big-icon c-topleft c-answering" />
    <Icon v-else-if="!connected && answering" icon="ph:wifi-slash-bold" class="big-icon c-topleft c-answering" />
    <Icon v-else-if="connected && !answering" icon="ph:wifi-high-bold" class="big-icon c-topleft" />
    <Icon v-else icon="ph:wifi-slash-bold" class="big-icon c-topleft" />
    <div class="c-bottomright1 c-clickable" >
    <Icon v-if="soundAlert" icon="fluent:speaker-2-20-filled" class="big-icon c-bottomright1 c-clickable" @click="toggleSoundAlertHandler" />
    <Icon v-else icon="fluent:speaker-off-20-filled" class="big-icon" @click="toggleSoundAlertHandler" />
    </div>


</template>
  
  <script>
  import { Icon } from '@iconify/vue';
  export default { 
    props: ['connected','answering','soundAlert'], 
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
  position: absolute;
  bottom: 0px;
  right: 0px;
}

svg {
   font-size: 24px;
   line-height: 1em;
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
