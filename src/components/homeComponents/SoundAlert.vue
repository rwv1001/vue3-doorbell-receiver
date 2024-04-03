<template>

   <Icon  icon="ph:wifi-slash-bold" class="big-icon c-bottomright2 " />

</template>


<script>
import { Icon } from '@iconify/vue';

export default {
  name: 'SoundAlert',
  props: ['soundAlertStatus'],
  methods: {
    toggleSound(){
      this.$emit('toggleSound');
    }
  }
}
</script>

<style>
.c-bottomright2 {
  position: absolute;
  bottom: 20px;
  right: 0px;
}
svg {
   font-size: 24px;
   line-height: 1em;
}

.big-icon {
   font-size: 100px;
}
</style>

