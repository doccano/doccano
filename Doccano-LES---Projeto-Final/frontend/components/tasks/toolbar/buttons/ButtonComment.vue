<template>
  <v-tooltip bottom>
    <template #activator="{ on }">
      <v-btn icon v-on="on" @click="$emit('click:comment')">
        <v-icon>
          {{ mdiMessageText }}
        </v-icon>
      </v-btn>
    </template>
    <span>{{ $t('annotation.commentTooltip') }}</span>
  </v-tooltip>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiMessageText } from '@mdi/js'

export default Vue.extend({
  data() {
    return {
      mdiMessageText
    }
  }
})
</script>
