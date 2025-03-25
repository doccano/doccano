<template>
    <v-card>
      <v-card-title>{{ $t('Delete') }}</v-card-title>
      <v-card-text>
        <p>{{ $t('Are you absolutely certain you want to permanently remove this user?') }}</p>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="$emit('cancel')">{{ $t('generic.cancel') }}</v-btn>
        <v-btn color="red" @click="$emit('remove')">{{ $t('generic.delete') }}</v-btn>
      </v-card-actions>
    </v-card>
  </template>
  
  <script lang="ts">
  import Vue from 'vue';
  export default Vue.extend({});
  </script>
  