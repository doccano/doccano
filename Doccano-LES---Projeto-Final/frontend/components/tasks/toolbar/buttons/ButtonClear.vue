<template>
  <v-tooltip bottom>
    <template #activator="{ on }">
      <v-btn icon v-on="on" @click="$emit('click:clear')">
        <v-icon>
          {{ mdiDeleteOutline }}
        </v-icon>
      </v-btn>
    </template>
    <span>Clear labels</span>
  </v-tooltip>
</template>

<script>
import { mdiDeleteOutline } from '@mdi/js'

export default {
  data() {
    return {
      mdiDeleteOutline
    }
  }
}
</script>
