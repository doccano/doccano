<template>
  <v-tooltip bottom>
    <template #activator="{ on }">
      <v-btn icon v-on="on" @click="$emit('click:guideline')">
        <v-icon>
          {{ mdiBookOpenOutline }}
        </v-icon>
      </v-btn>
    </template>
    <span>{{ $t('annotation.guidelineTooltip') }}</span>
  </v-tooltip>
</template>

<script>
import { mdiBookOpenOutline } from '@mdi/js'

export default {
  data() {
    return {
      mdiBookOpenOutline
    }
  }
}
</script>
