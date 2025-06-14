<template>
  <v-stepper-header>
    <v-stepper-step :complete="step > 1" step="1"> Select a template </v-stepper-step>
    <v-divider />
    <v-stepper-step :complete="step > 2" step="2"> Set parameters </v-stepper-step>
    <v-divider />
    <v-stepper-step :complete="step > 3" step="3"> Set a template </v-stepper-step>
    <v-divider />
    <v-stepper-step :complete="step > 4" step="4"> Set mappings </v-stepper-step>
  </v-stepper-header>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  props: {
    step: {
      type: Number,
      default: 1,
      required: true
    }
  }
})
</script>
