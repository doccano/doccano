<template>
  <v-text-field
    v-bind="$attrs"
    :value="value"
    :rules="descriptionRules($t('rules.descriptionRules'))"
    :label="$t('generic.description')"
    required
    @input="$emit('input', $event)"
  />
</template>

<script lang="ts">
import { descriptionRules } from '@/rules/index'
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
      descriptionRules
    }
  }
})
</script>
