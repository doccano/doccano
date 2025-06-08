<template>
  <v-card
  max-width="500"
  class="rounded-lg elevation-10 mx-auto"
>
    <!-- Topo azul com título -->
    <v-toolbar color="primary white--text" flat>
      <v-toolbar-title>{{ title }}</v-toolbar-title>
    </v-toolbar>

    <!-- Corpo do conteúdo -->
    <v-card-text class="text--primary px-5 py-4">
      <slot name="content" />
    </v-card-text>

    <!-- Botões alinhados -->
    <v-card-actions class="px-5 pb-4">
      <v-spacer />
      <v-btn
        v-if="cancelText"
        class="text-capitalize"
        text
        color="primary"
        data-test="cancel-button"
        @click="cancel"
      >
        {{ cancelText }}
      </v-btn>
      <v-btn
        v-if="agreeText"
        :disabled="disabled"
        class="text-none"
        text
        color="error"
        data-test="delete-button"
        @click="agree"
      >
        {{ agreeText }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>


<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  props: {
    title: {
      type: String,
      default: '',
      required: true
    },
    cancelText: {
      type: String,
      default: ''
    },
    agreeText: {
      type: String,
      default: ''
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
})
</script>
