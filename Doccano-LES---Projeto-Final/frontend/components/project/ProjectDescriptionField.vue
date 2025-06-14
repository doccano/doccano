<template>
  <v-text-field
    v-bind="$attrs"
    :value="value"
    :rules="descriptionRules"
    :label="$t('generic.description')"
    required
    @input="$emit('input', $event)"
  />
</template>

<script lang="ts">
import Vue from 'vue'
import { validateMinLength } from '~/domain/models/project/project'

export default Vue.extend({
  props: {
    value: {
      type: String,
      default: '',
      required: true
    }
  },
  data() {
    return {
      descriptionRules: [
        (text: string) => validateMinLength(text) || this.$t('rules.description.required')
      ]
    }
  }
})
</script>
