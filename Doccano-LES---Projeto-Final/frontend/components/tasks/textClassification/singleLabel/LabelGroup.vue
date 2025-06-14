<template>
  <v-chip-group :value="annotatedLabel" column @change="addOrRemove">
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
      return this.labels.findIndex((item) => labelIds.includes(item.id))
    }
  },

  methods: {
    addOrRemove(index) {
      if (index === undefined) {
        const label = this.labels[this.annotatedLabel]
        this.remove(label)
      } else {
        const label = this.labels[index]
        this.add(label)
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
