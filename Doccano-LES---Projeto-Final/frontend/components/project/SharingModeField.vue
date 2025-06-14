<template>
  <v-checkbox
    v-bind="$attrs"
    :value="value"
    :label="$t('overview.shareAnnotations')"
    @change="$emit('input', $event === true)"
  />
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  props: {
    value: {
      type: Boolean,
      default: false,
      required: true
    }
  }
})
</script>
