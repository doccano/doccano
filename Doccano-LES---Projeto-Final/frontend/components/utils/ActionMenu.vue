<template>
  <v-menu offset-y open-on-hover>
    <template #activator="{ on }">
      <v-btn color="primary text-capitalize" v-on="on">
        {{ text }}
        <v-icon>{{ mdiMenuDown }}</v-icon>
      </v-btn>
    </template>
    <v-list>
      <v-list-item v-for="(item, index) in items" :key="index" @click="$emit(item.event)">
        <v-list-item-icon>
          <v-icon>{{ item.icon }}</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiMenuDown } from '@mdi/js'

export default Vue.extend({
  props: {
    text: {
      type: String,
      default: 'Actions'
    },
    items: {
      type: Array,
      default: () => [],
      required: true
    }
  },

  data() {
    return {
      mdiMenuDown
    }
  }
})
</script>
