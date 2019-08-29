<template>
  <v-card>
    <v-card-title class="grey lighten-2">
      {{ title }}
    </v-card-title>
    <v-container grid-list-sm>
      <v-layout wrap>
        <v-flex xs12>
          <slot name="content" />
        </v-flex>
      </v-layout>
    </v-container>
    <v-card-actions>
      <v-spacer />
      <v-btn
        class="text-capitalize"
        text
        color="primary"
        @click="cancel"
      >
        Cancel
      </v-btn>
      <v-btn
        :disabled="disabled"
        class="text-none"
        text
        @click="agree"
      >
        {{ button }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      default: '',
      required: true
    },
    button: {
      type: String,
      default: '',
      required: true
    },
    disabled: {
      type: Boolean,
      default: false,
      required: true
    }
  },
  methods: {
    cancel() {
      this.$emit('cancel')
    },
    agree() {
      this.$emit('agree')
    }
  }
}
</script>
