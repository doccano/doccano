<template>
  <v-combobox
    v-model="annotatedLabels"
    chips
    :items="mappingLabels"
    item-text="text"
    hide-details
    hide-selected
    multiple
    class="pt-0"
    :search-input.sync="search"
    @change="search = ''"
  >
    <template v-slot:selection="{ attrs, item, select, selected }">
      <v-chip
        v-bind="attrs"
        :input-value="selected"
        :color="item.backgroundColor"
        :text-color="$contrastColor(item.backgroundColor)"
        close
        @click="select"
        @click:close="remove(item)"
      >
        <v-avatar left color="white" class="black--text font-weight-bold">
          {{ item.suffixKey }}
        </v-avatar>
          {{ item.text }}
      </v-chip>
    </template>
    <template v-slot:item="{ item }">
      <v-chip
        :color="item.backgroundColor"
        :text-color="$contrastColor(item.backgroundColor)"
      >
        <v-avatar left color="white" class="black--text font-weight-bold">
          {{ item.suffixKey }}
        </v-avatar>
             {{ item.text }} 
      </v-chip>
    </template>
  </v-combobox>
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
      default: () => ([]),
      required: true
    },
    text: {
      type: String,
      default: '',
      required: true
    }
  },

  data() {
    return {
      search: ''
    }
  },

  computed: {
    mappingLabels() {
      return this.getLabel(this.labels)
    },
    annotatedLabels: {
      get() {
        const labelIds = this.annotations.map(item => item.label)
        const labels = this.labels.filter(item => labelIds.includes(item.id))
        return this.getLabel(labels)
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
            this.remove(label)
          }
        }
      }
    },
    getLabelMap() {
      let map = []
      try {
        map = JSON.parse(this.text.match(/(?<=@taboola-doccano-concept ).*/)[0]).concepts
      } catch (error) { }
      return map
    },
  },

  methods: {
    add(label) {
      this.$emit('add', label.id)
    },

    remove(label) {
      const annotation = this.annotations.find(item => item.label === label.id)
      this.$emit('remove', annotation.id)
    },

    getLabel(labels) {
      if (this.text.startsWith('@taboola-doccano-concept')){
          return labels.map(it=>{
            return {
              ...it,
              text:this.getLabelMap[it.text].text
            }
          })
      }else{
        return labels
      }
    }
  }
}
</script>
