<template>
  <v-combobox
    v-model="annotatedLabels"
    chips
    :items="labels"
    item-text="text"
    hide-details
    hide-selected
    multiple
    class="pt-0"
    :search-input.sync="search"
    @change="search = ''"
  >
    <template #selection="{ attrs, item, select, selected }">
      <v-chip
        v-bind="attrs"
        :input-value="selected"
        :color="item.backgroundColor"
        :text-color="$contrastColor(item.backgroundColor)"
        close
        @click="select"
        @click:close="remove(item)"
      >
        <v-avatar v-if="item.suffixKey" left color="white" class="black--text font-weight-bold">
          {{ item.suffixKey }}
        </v-avatar>
        {{ item.text }}
      </v-chip>
    </template>
    <template #item="{ item }">
      <v-chip :color="item.backgroundColor" :text-color="$contrastColor(item.backgroundColor)">
        <v-avatar v-if="item.suffixKey" left color="white" class="black--text font-weight-bold">
          {{ item.suffixKey }}
        </v-avatar>
        {{ item.text }}
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
    },
    annotations: {
      type: Array,
      default: () => [],
      required: true
    }
  },

  data() {
    return {
      search: ''
    }
  },

  computed: {
    annotatedLabels: {
      get() {
        const labelIds = this.annotations.map((item) => item.label)
        return this.labels.filter((item) => labelIds.includes(item.id))
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
          const label = this.annotatedLabels.find((x) => !newValue.some((y) => y.id === x.id))
          if (typeof label === 'object') {
            this.remove(label)
          }
        }
      }
    }
  },

  methods: {
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
