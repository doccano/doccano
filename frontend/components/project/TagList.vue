<template>
  <v-combobox
    v-bind="$attrs"
    :value="value"
    :items="value"
    label="Tags"
    multiple
    chips
    outlined
    dense
    deletable-chips
    hide-selected
    @change="$emit('input', $event)"
  />
</template>

<script lang="ts">
import Vue, { PropType } from 'vue'
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
