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
        data-test="cancel-button"
        @click="cancel"
      >
        {{ cancelText }}
      </v-btn>
      <v-btn
        class="text-none"
        text
        :disabled="disabled"
        data-test="delete-button"
        @click="agree"
      >
        {{ agreeText }}
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
    cancelText: {
      type: String,
      default: '',
      required: true
    },
    agreeText: {
      type: String,
      default: '',
      required: true
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },

  methods: {
    agree() {
      this.$emit('agree')
    },
    cancel() {
      this.$emit('cancel')
    }
  }
}
</script>
