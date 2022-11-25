<template>
  <v-text-field
    v-bind="$attrs"
    :value="value"
    :rules="projectNameRules"
    :label="$t('overview.projectName')"
    required
    @input="$emit('input', $event)"
  />
</template>

<script lang="ts">
import Vue from 'vue'
import { validateMinLength, validateNameMaxLength } from '~/domain/models/project/project'

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
      projectNameRules: [
        (text: string) => validateMinLength(text) || this.$t('rules.projectName.required'),
        (text: string) => validateNameMaxLength(text) || this.$t('rules.projectName.maxLength')
      ]
    }
  }
})
</script>
