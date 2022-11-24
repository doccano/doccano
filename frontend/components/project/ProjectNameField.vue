<template>
  <v-text-field
    v-bind="$attrs"
    :value="value"
    :rules="projectNameRules($t('rules.projectNameRules'))"
    :label="$t('overview.projectName')"
    required
    @input="$emit('input', $event)"
  />
</template>

<script lang="ts">
import { projectNameRules } from '@/rules/index'
import Vue from 'vue'

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
      projectNameRules
    }
  }
})
</script>
