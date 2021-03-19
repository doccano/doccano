<template>
  <v-select
    :value="annotatedLabel"
    :items="labels"
    item-text="text"
    :label="$t('labels.labels')"
    hide-selected
    return-object
    chips
    @change="addOrRemove"
  >
    <template v-slot:selection="{ attrs, item, select, selected }">
      <v-chip
        v-if="item.backgroundColor"
        v-bind="attrs"
        :input-value="selected"
        :color="item.backgroundColor"
        :text-color="$contrastColor(item.backgroundColor)"
        close
        @click="select"
        @click:close="remove(item)"
      >
        {{ item.text }}
      </v-chip>
    </template>
  </v-select>
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
      default: () => ([]),
      required: true
    }
  },

  computed: {
    annotatedLabel() {
      const labelIds = this.annotations.map(item => item.label)
      return this.labels.find(item => labelIds.includes(item.id))
    }
  },

  methods: {
    addOrRemove(val) {
      if (val) {
        this.add(val)
      } else {
        this.remove(this.annotatedLabel)
      }
    },

    add(label) {
      this.$emit('add', label.id)
    },

    remove(label) {
      const annotation = this.annotations.find(item => item.label === label.id)
      this.$emit('remove', annotation.id)
    }
  }
}
</script>
