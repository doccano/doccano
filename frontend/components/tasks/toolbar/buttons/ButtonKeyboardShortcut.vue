<template>
  <v-tooltip bottom>
    <template #activator="{ on }">
      <v-btn icon v-on="on" @click="$emit('click:open')">
        <v-icon>
          {{ mdiKeyboardOutline }}
        </v-icon>
      </v-btn>
    </template>
    <span>Keyboard Shortcut</span>
  </v-tooltip>
</template>

<script>
import { mdiKeyboardOutline } from '@mdi/js'

export default {
  data() {
    return {
      mdiKeyboardOutline
    }
  }
}
</script>
