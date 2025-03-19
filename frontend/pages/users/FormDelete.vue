<template>
    <v-card>
      <v-card-title>
        {{ $t('user.deleteConfirmation') }}
      </v-card-title>
      <v-card-text>
        {{ $t('user.deleteConfirmationMessage', { count: selected.length }) }}
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="$emit('cancel')">
          {{ $t('generic.cancel') }}
        </v-btn>
        <v-btn color="error" text @click="$emit('remove')">
          {{ $t('generic.delete') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </template>
  
  <script lang="ts">
  import Vue from 'vue';
  
  export default Vue.extend({
    props: {
      selected: {
        type: Array,
        required: true,
      },
    },
  });
  </script>