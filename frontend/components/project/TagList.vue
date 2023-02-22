<template>
  <v-combobox
    v-bind="$attrs"
    :value="value"
    :items="value"
    label="Tags"
    multiple
    chips
    deletable-chips
    hide-selected
    hide-details
    @change="$emit('input', $event)"
  />
</template>

<script lang="ts">
import type { PropType } from 'vue'
import Vue from 'vue'
export default Vue.extend({
  props: {
    value: {
      type: Array as PropType<string[]>,
      default: () => [],
      required: true
    }
  }
})
</script>
