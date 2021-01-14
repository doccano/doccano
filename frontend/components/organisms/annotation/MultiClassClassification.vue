<template>
  <v-combobox
    v-model="annotatedLabels"
    :items="labels"
    item-text="text"
    label="Label"
    hide-selected
    chips
    multiple
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
    annotatedLabels: {
      get() {
        const labelIds = this.annotations.map(item => item.label)
        return this.labels.filter(item => labelIds.includes(item.id))
      },
      set(newValue) {
        if (newValue.length > this.annotations.length) {
          const label = newValue[newValue.length - 1]
          if (typeof label === 'object') {
            this.add(label)
          } else {
            newValue.pop()
          }
        } else {
          const label = this.annotatedLabels.find(x => !newValue.some(y => y.id === x.id))
          if (typeof label === 'object') {
            this.remove(label.id)
          }
        }
      }
    }
  },

  methods: {
    textColor(backgroundColor) {
      return idealColor(backgroundColor)
    },
    add(label) {
      this.addLabel(label.id)
    },
    remove(labelId) {
      const annotation = this.annotations.find(item => item.label === labelId)
      this.deleteLabel(annotation.id)
    }
  }
}
</script>
