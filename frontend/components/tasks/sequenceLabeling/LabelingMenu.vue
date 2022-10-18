<template>
  <v-menu :value="opened" :position-x="x" :position-y="y" absolute offset-y @input="close">
    <v-list dense min-width="150" max-height="400" class="overflow-y-auto">
      <v-list-item>
        <v-autocomplete
          ref="autocomplete"
          v-model="value"
          :items="labels"
          autofocus
          dense
          deletable-chips
          hide-details
          item-text="text"
          item-value="id"
          label="Select a label"
          small-chips
        />
      </v-list-item>
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
      <v-list-item v-for="(label, i) in labels" :key="i" @click="onLabelSelected(label.id)">
=======
      <v-list-item v-for="(label, i) in labels.slice(0,100)" :key="i" @click="onLabelSelected(label.id)">
>>>>>>> da50a415 (Limited label dropdown to display first 100 labels)
=======
      <!-- <v-list-item v-for="(label, i) in labels.slice(0,100)" :key="i" @click="onLabelSelected(label.id)">
>>>>>>> 8d1f4d31 (Removed remaining labels from the dropdown menu)
=======
      <v-list-item v-for="(label, i) in labels.slice(0,100)" :key="i" @click="onLabelSelected(label.id)">
>>>>>>> 0b78e227 (Added label description)
        <v-list-item-action v-if="hasAnySuffixKey">
          <v-chip
            v-if="label.suffixKey"
            :color="label.backgroundColor"
            outlined
            small
            text="#"
          />
          <span v-else class="mr-8" />
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title v-text="label.text" />
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  props: {
    labels: {
      type: Array,
      default: () => [],
      required: true
    },
    opened: {
      type: Boolean,
      default: false,
      required: true
    },
    selectedLabel: {
      type: Object,
      default: null,
      required: false
    },
    x: {
      type: Number,
      default: 0,
      required: true
    },
    y: {
      type: Number,
      default: 0,
      required: true
    }
  },

  data() {
    return {
      startOffset: 0,
      endOffset: 0,
      entity: null as any,
      fromEntity: null as any,
      toEntity: null as any
    }
  },

  computed: {
    hasAnySuffixKey(): boolean {
      return this.labels.some((label: any) => label.suffixKey !== null)
    },

    value: {
      get() {
        return this.selectedLabel
      },
      set(labelId: number) {
        this.onLabelSelected(labelId)
      }
    }
  },

  methods: {
    close() {
      // Todo: a bit hacky. I want to fix this problem.
      // https://github.com/vuetifyjs/vuetify/issues/10765
      this.$nextTick(() => {
        if (this.$refs.autocomplete) {
          ;(this.$refs.autocomplete as any).selectedItems = []
        }
      })
      this.$emit('close')
    },

    onLabelSelected(labelId: number) {
      this.$emit('click:label', labelId)
      this.close()
    }
  }
})
</script>
