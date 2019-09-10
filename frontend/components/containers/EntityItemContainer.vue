<template>
  <div class="highlight-container highlight-container--bottom-labels" @mouseup="open">
    <entity-item v-for="(chunk, i) in chunks" :key="i" :content="chunk.text" :label="chunk.label" :color="chunk.color" />
  </div>
</template>

<script>
import EntityItem from '~/components/molecules/EntityItem'

export default {
  components: {
    EntityItem
  },
  props: {
    content: {
      type: String,
      default: '',
      required: true
    },
    labels: {
      type: Array,
      default: () => ([]),
      required: true
    },
    entities: {
      type: Array,
      default: () => ([]),
      required: true
    }
  },
  computed: {
    sortedEntities() {
      return this.entities.slice().sort((a, b) => a.start_offset - b.start_offset)
    },

    chunks() {
      const chunks = []
      const entities = this.sortedEntities
      let startOffset = 0
      for (const entity of entities) {
        // add non-entities to chunks.
        chunks.push({
          label: null,
          color: null,
          text: this.content.slice(startOffset, entity.start_offset)
        })
        startOffset = entity.end_offset

        // add entities to chunks.
        const label = this.labelObject[entity.label]
        chunks.push({
          label: label.name,
          color: label.color,
          text: this.content.slice(entity.start_offset, entity.end_offset)
        })
      }
      // add the rest of text.
      chunks.push({
        label: null,
        color: null,
        text: this.content.slice(startOffset, this.content.length)
      })
      return chunks
    },

    labelObject() {
      const obj = {}
      for (const label of this.labels) {
        obj[label.id] = label
      }
      return obj
    }
  },
  methods: {
    open() {
      let selection
      // Modern browsers.
      if (window.getSelection) {
        selection = window.getSelection()
      } else if (document.selection) {
        selection = document.selection
      }
      // If something is selected.
      if (selection.rangeCount > 0) {
        const range = selection.getRangeAt(0)
        const preSelectionRange = range.cloneRange()
        preSelectionRange.selectNodeContents(this.$el)
        preSelectionRange.setEnd(range.startContainer, range.startOffset)
        const start = [...preSelectionRange.toString()].length
        const end = start + [...range.toString()].length
        alert(start + ' ' + end)
        return end
      }
    }
  }
}
</script>

<style scoped>
.highlight-container.highlight-container--bottom-labels {
    align-items: flex-start;
}
.highlight-container {
    line-height: 42px!important;
    display: flex;
    flex-wrap: wrap;
    white-space: pre-wrap;
    cursor: default;
}
.highlight-container.highlight-container--bottom-labels .highlight.bottom {
    margin-top: 6px;
}
</style>
