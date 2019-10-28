<template>
  <v-combobox
    :value="annotatedLabels"
    :items="labels"
    item-text="text"
    label="Label"
    hide-selected
    chips
    multiple
    @input="add"
  >
    <template v-slot:selection="{ attrs, item, select, selected }">
      <v-chip
        v-bind="attrs"
        :input-value="selected"
        :color="item.background_color"
        :text-color="textColor(item.background_color)"
        close
        @click="select"
        @click:close="remove(item.id)"
      >
        {{ item.text }}
      </v-chip>
    </template>
  </v-combobox>
</template>

<script>
import { idealColor } from '~/plugins/utils'

export default {
  props: {
    labels: {
      type: Array,
      default: () => [],
      required: true
    },
    annotations: {
      type: Array,
      default: () => ([]),
      required: true
    },
    addLabel: {
      type: Function,
      default: () => ([]),
      required: true
    },
    deleteLabel: {
      type: Function,
      default: () => ([]),
      required: true
    }
  },

  computed: {
    annotatedLabels() {
      const labelIds = this.annotations.map(item => item.label)
      return this.labels.filter(item => labelIds.includes(item.id))
    },
    labelObject() {
      const obj = {}
      for (const label of this.labels) {
        obj[label.id] = label
      }
      return obj
    }
  },

  methods: {
    textColor(backgroundColor) {
      return idealColor(backgroundColor)
    },
    add(labels) {
      const label = labels[labels.length - 1]
      this.addLabel(label.id)
    },
    remove(labelId) {
      const annotation = this.annotations.find(item => item.label === labelId)
      this.deleteLabel(annotation.id)
    }
  }
}
</script>
