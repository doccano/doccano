<template>
  <v-chip-group
    :value="annotatedLabel"
    column
    multiple
    @change="addOrRemove"
  >
    <v-chip
      v-for="(item, index) in labels"
      :key="item.id"
      :color="item.backgroundColor"
      filter
      :text-color="$contrastColor(item.backgroundColor)"
    >
      {{getLabelText(item,index)}}
      <v-avatar
        right
        color="white"
        class="black--text font-weight-bold"
      >
        {{ item.suffixKey }}
      </v-avatar>
    </v-chip>
  </v-chip-group>
</template>

<script>
import _ from 'lodash'
import { conceptToken } from "@/app.config.js"

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

  computed: {
    annotatedLabel() {
      const labelIds = this.annotations.map(item => item.label)
      return labelIds.map(id => this.labels.findIndex(item => item.id === id))
    },
    getLabelMap() {
      let map = []
      try {
        const reg = new RegExp( '(?<=' + conceptToken + ' ).*', 'g')
        map = JSON.parse(this.text.match(reg)[0]).concepts
      } catch (error) { }
      return map
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
      if(_.get(label,'id',false)!==false){
         this.$emit('add', label.id)
      }
  
    },

    remove(label) {
      if(_.get(label,'id',false)!==false){
        const annotation = this.annotations.find(item => item.label === label.id)
        this.$emit('remove', annotation.id)
      }
    },

    getLabelText(item,index) {
      if (this.text.startsWith(conceptToken)){
         return _.get(this,`getLabelMap[${index}].text`,"")
      }else{
        return item.text
      }
    }
  }
}
</script>
