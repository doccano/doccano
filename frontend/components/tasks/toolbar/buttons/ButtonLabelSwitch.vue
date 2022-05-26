<template>
  <v-btn-toggle v-model="option" mandatory>
    <v-btn icon>
      <v-icon>{{ mdiFormatListBulleted }}</v-icon>
    </v-btn>
    <v-btn icon>
      <v-icon>{{ mdiText }}</v-icon>
    </v-btn>
  </v-btn-toggle>
</template>

<script>
import { mdiFormatListBulleted, mdiText } from '@mdi/js'

export default {
  data() {
    return {
      option: 0,
      mdiFormatListBulleted,
      mdiText
    }
  },

  watch: {
    option(val) {
      if (val === 0) {
        this.$emit('change', 'label-group')
      } else {
        this.$emit('change', 'label-select')
      }
    }
  }
}
</script>
