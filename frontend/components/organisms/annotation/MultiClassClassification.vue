<template>
  <v-combobox
    v-model="annotatedLabels"
    :items="labels"
    item-text="text"
    :label="$t('labels.labels')"
    hide-selected
    chips
    :disabled="isAdding"
    :search-input.sync="search"
    @change="search=''"
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

  data() {
    return {
      search: '',
      isAdding: false
    }
  },

  computed: {
    annotatedLabels: {
      get() {
        const labelIds = this.annotations.map(item => item.label)
        return this.labels.find(item => labelIds.includes(item.id))
      },
      set(newValue) {
        console.log('set: start')
        this.isAdding = true
        if (this.annotations.length === 1) {
          this.remove(this.annotations[0].label)
        }

        this.add(newValue).then((r) => {
          console.log('set: add ok', r)
          this.isAdding = false
        })
      }
    }
  },

  methods: {
    textColor(backgroundColor) {
      return idealColor(backgroundColor)
    },
    add(label) {
      return this.addLabel(label.id)
    },
    remove(labelId) {
      const annotation = this.annotations.find(item => item.label === labelId)
      this.deleteLabel(annotation.id)
    }
  }
}
</script>
