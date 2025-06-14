<template>
  <label-group-single
    v-if="singleLabel"
    :annotations="annotations"
    :labels="labels"
    @add="$emit('add', $event)"
    @remove="$emit('remove', $event)"
  />
  <label-group-multi
    v-else
    :annotations="annotations"
    :labels="labels"
    @add="$emit('add', $event)"
    @remove="$emit('remove', $event)"
  />
</template>

<script>
import LabelGroupSingle from './singleLabel/LabelGroup.vue'
import LabelGroupMulti from './multiLabel/LabelGroup.vue'

export default {
  components: {
    LabelGroupSingle,
    LabelGroupMulti
  },

  props: {
    labels: {
      type: Array,
      default: () => [],
      required: true
    },
    annotations: {
      type: Array,
      default: () => [],
      required: true
    },
    singleLabel: {
      type: Boolean,
      default: false,
      required: true
    }
  }
}
</script>
