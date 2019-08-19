<template>
  <v-dialog
    v-model="dialog"
    width="800px"
  >
    <v-card>
      <v-card-title class="grey lighten-2">
        {{ title }}
      </v-card-title>
      <v-container grid-list-sm>
        <v-layout
          wrap
        >
          <v-flex xs12>
            <slot />
          </v-flex>
        </v-layout>
      </v-container>
      <v-card-actions>
        <v-spacer />
        <v-btn
          class="text-capitalize"
          text
          color="primary"
          @click="dialog = false"
        >
          Cancel
        </v-btn>
        <v-btn
          class="text-none"
          text
          @click="dialog = false"
        >
          {{ button }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      default: ''
    },
    button: {
      type: String,
      default: 'Yes'
    }
  },
  data: () => ({
    dialog: false
  }),
  methods: {
    open() {
      this.dialog = true
    },
    agree() {
      this.dialog = false
    },
    cancel() {
      this.dialog = false
    }
  }
}
</script>
