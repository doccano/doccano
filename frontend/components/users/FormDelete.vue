<template>
    <v-card>
      <v-card-title>{{ $t('generic.delete') }}</v-card-title>
      <v-card-text>
        <p>{{ $t('user.confirmDelete') }}</p>
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
  