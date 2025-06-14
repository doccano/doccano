<template>
  <v-btn-toggle mandatory>
    <v-tooltip bottom>
      <template #activator="{ on }">
        <v-btn icon @click="$emit('zoom-out')" v-on="on">
          <v-icon>{{ mdiMagnifyMinusOutline }}</v-icon>
        </v-btn>
      </template>
      <span>Zoom Out</span>
    </v-tooltip>
    <v-tooltip bottom>
      <template #activator="{ on }" v-on="on">
        <v-btn icon @click="$emit('zoom-in')">
          <v-icon>{{ mdiMagnifyPlusOutline }}</v-icon>
        </v-btn>
      </template>
      <span>Zoom In</span>
    </v-tooltip>
  </v-btn-toggle>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiMagnifyPlusOutline, mdiMagnifyMinusOutline } from '@mdi/js'
export default Vue.extend({
  data() {
    return {
      mdiMagnifyPlusOutline,
      mdiMagnifyMinusOutline
    }
  }
})
</script>
