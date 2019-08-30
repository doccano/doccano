<template>
  <v-dialog
    v-model="dialog"
    width="800px"
  >
    <template v-slot:activator="{ on }">
      <v-btn
        class="mb-2 text-capitalize"
        color="primary"
        @click="dialog=true"
      >
        {{ text }}
      </v-btn>
    </template>
    <template #content />
  </v-dialog>
</template>

<script>
export default {
  props: {
    text: {
      type: String,
      default: '',
      required: true
    }
  },

  data() {
    return {
      dialog: false
    }
  }
}
</script>
