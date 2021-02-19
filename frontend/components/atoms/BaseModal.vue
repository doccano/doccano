<template>
  <v-dialog
    v-model="dialog"
    width="800px"
  >
    <template v-slot:activator="{ }">
      <slot name="opener" :open="open" />
    </template>
    <slot name="content" :close="close" />
  </v-dialog>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  data() {
    return {
      dialog: false as Boolean
    }
  },

  methods: {
    close(): void {
      this.dialog = false
    },
    open(): void {
      this.dialog = true
    }
  }
})
</script>
