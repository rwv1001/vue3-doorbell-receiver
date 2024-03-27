<template>
    
    <Icon v-if="connected" icon="ph:wifi-high-bold" class="big-icon c-topleft" />
    <Icon v-else icon="ph:wifi-slash-bold" class="big-icon c-topleft" />

</template>
  
  <script>
 // import { state } from "@/main";
  import { Icon } from '@iconify/vue';
 // import { ref, watch , computed} from "vue";
 // const connectState = ref(false);
  export default { 
    props: ['connected'],   
    // computed: {
    //   connected() {
    //     console.log("computed state = "+ state.connected)
    //     connectState = state.connected;
    //     return state.connected;
    //   }
    // },
    components: {
      Icon,
    },
    name: 'BaseConnection',
    mounted() {
      // watch(connectState, () => {
      //   console.log("watch state.connected = " + state.connected)
      // })

    },
    data() {

   
    },

  }
  </script>
  
  <style>
  .c-topleft {
  position: absolute;
  top: 0px;
  left: 0px;
}

svg {
   font-size: 24px;
   line-height: 1em;
}

.big-icon {
   font-size: 100px;
}
  </style>