<template>
  <v-tooltip bottom>
    <template #activator="{ on }">
      <v-btn icon v-on="on" @click="$emit('click:auto')">
        <v-icon>
          {{ mdiAutoFix }}
        </v-icon>
      </v-btn>
    </template>
    <span>Auto Labeling</span>
  </v-tooltip>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiAutoFix } from '@mdi/js'

export default Vue.extend({
  data() {
    return {
      mdiAutoFix
    }
  }
})
</script>
