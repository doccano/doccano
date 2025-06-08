<template>
  <v-dialog :value="visible" max-width="420" @input="$emit('close')">
    <v-card class="rounded-lg elevation-10">
      <v-card-title class="white--text d-flex align-center" style="background-color: #f44336cc;">
        <v-icon left class="mr-2">mdi-alert-circle</v-icon>
        <span class="headline">Error</span>
      </v-card-title>
      <v-card-text class="pa-5 text-body-1 grey--text text--darken-3">
        {{ message }}
      </v-card-text>
      <v-card-actions class="px-5 pb-4">
        <v-spacer></v-spacer>
        <v-btn text class="red--text" @click="$emit('close')">OK</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
export default {
  name: 'ErrorDialog',
  props: {
    visible: {
      type: Boolean,
      required: true
    },
    message: {
      type: String,
      default: ''
    }
  }
}
</script>
