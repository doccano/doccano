<template>
  <v-combobox
    v-model="chips"
    :items="labels"
    chips
    clearable
    label="Label"
    multiple
  >
    <template v-slot:selection="{ attrs, item, select, selected }">
      <v-chip
        v-bind="attrs"
        :input-value="selected"
        close
        @click="select"
        @click:close="remove(item)"
      >
        {{ item }}
      </v-chip>
    </template>
  </v-combobox>
</template>

<script>
export default {
  props: {
    labels: {
      type: Array,
      default: () => [],
      required: true
    }
  },

  data() {
    return {
      chips: []
    }
  },

  methods: {
    remove(item) {
      this.chips.splice(this.chips.indexOf(item), 1)
      this.chips = [...this.chips]
    }
  }
}
</script>
