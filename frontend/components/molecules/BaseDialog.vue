<template>
  <v-dialog
    :value="dialog"
    :width="width"
  >
    <slot />
  </v-dialog>
</template>

<script>
export default {
  props: {
    dialog: {
      type: Boolean,
      default: false,
      required: true
    },
    width: {
      type: String,
      default: '800'
    }
  }
}
</script>
