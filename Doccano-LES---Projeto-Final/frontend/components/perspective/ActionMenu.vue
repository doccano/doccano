<template>
  <v-btn 
    color="primary" 
    class="text-capitalize" 
    :disabled="disabled"
    @click="$emit('create')"
  >
    Create Perspective
  </v-btn>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  props: {
    disabled: {
      type: Boolean,
      default: false
    }
  }
})
</script>
