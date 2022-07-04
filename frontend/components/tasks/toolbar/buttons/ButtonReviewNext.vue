<template>
  <v-tooltip bottom>
    <template #activator="{ on }">
      <v-btn
        v-shortkey.once="['alt', 'enter']"
        icon
        v-on="on"
        @shortkey="$emit('click:review-next')"
        @click="$emit('click:review-next')"
      >
        <v-icon>
          {{ mdiAirplaneCheck }}
        </v-icon>
      </v-btn>
    </template>
    <span>Set reviewed & next [alt]+[enter]</span>
  </v-tooltip>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiAirplaneCheck } from '@mdi/js'

export default Vue.extend({
  data() {
    return {
      mdiAirplaneCheck
    }
  }
})
</script>
