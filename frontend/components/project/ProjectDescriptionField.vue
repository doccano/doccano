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
import { isEmptyText } from '~/domain/models/project/project'

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
        (text: string) =>
          !isEmptyText(text) || this.$t('rules.descriptionRules.descriptionRequired')
      ]
    }
  }
})
</script>
