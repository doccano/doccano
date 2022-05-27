<template>
  <v-chip-group :value="annotatedLabel" column multiple @change="addOrRemove">
    <v-chip
      v-for="item in labels"
      :key="item.id"
      :color="item.backgroundColor"
      filter
      :text-color="$contrastColor(item.backgroundColor)"
    >
      {{ item.text }}
      <v-avatar v-if="item.suffixKey" right color="white" class="black--text font-weight-bold">
        {{ item.suffixKey }}
      </v-avatar>
    </v-chip>
  </v-chip-group>
</template>

<script>
import _ from 'lodash'

export default {
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
    }
  },

  computed: {
    annotatedLabel() {
      const labelIds = this.annotations.map((item) => item.label)
      return labelIds.map((id) => this.labels.findIndex((item) => item.id === id))
    }
  },

  methods: {
    addOrRemove(indexes) {
      if (indexes.length > this.annotatedLabel.length) {
        const index = _.difference(indexes, this.annotatedLabel)
        const label = this.labels[index]
        this.add(label)
      } else {
        const index = _.difference(this.annotatedLabel, indexes)
        const label = this.labels[index]
        this.remove(label)
      }
    },

    add(label) {
      this.$emit('add', label.id)
    },

    remove(label) {
      const annotation = this.annotations.find((item) => item.label === label.id)
      this.$emit('remove', annotation.id)
    }
  }
}
</script>
