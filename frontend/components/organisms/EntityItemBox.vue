<template>
  <div class="highlight-container highlight-container--bottom-labels" @click="open">
    <entity-item
      v-for="(chunk, i) in chunks"
      :key="i"
      :content="chunk.text"
      :label="chunk.label"
      :color="chunk.color"
      :labels="labels"
      @remove="deleteAnnotation(chunk.id)"
      @update="updateEntity($event.id, chunk.id)"
    />
    <v-menu
      v-model="showMenu"
      :position-x="x"
      :position-y="y"
      absolute
      offset-y
    >
      <v-list
        dense
        min-width="150"
        max-height="400"
        class="overflow-y-auto"
      >
        <v-list-item
          v-for="(label, i) in labels"
          :key="i"
          @click="addEntity(start, end, label.id)"
        >
          <v-list-item-content>
            <v-list-item-title v-text="label.text" />
          </v-list-item-content>
          <v-list-item-action>
            <v-list-item-action-text v-text="label.suffix_key" />
          </v-list-item-action>
        </v-list-item>
      </v-list>
    </v-menu>
  </div>
</template>

<script>
import EntityItem from '~/components/molecules/EntityItem'

export default {
  components: {
    EntityItem
  },
  props: {
    text: {
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
    },
    deleteAnnotation: {
      type: Function,
      default: () => ([]),
      required: true
    },
    updateEntity: {
      type: Function,
      default: () => ([]),
      required: true
    },
    addEntity: {
      type: Function,
      default: () => ([]),
      required: true
    }
  },
  data() {
    return {
      showMenu: false,
      x: 0,
      y: 0,
      start: 0,
      end: 0
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
          text: this.text.slice(startOffset, entity.start_offset)
        })
        startOffset = entity.end_offset

        // add entities to chunks.
        const label = this.labelObject[entity.label]
        chunks.push({
          id: entity.id,
          label: label.text,
          color: label.background_color,
          text: this.text.slice(entity.start_offset, entity.end_offset)
        })
      }
      // add the rest of text.
      chunks.push({
        label: null,
        color: null,
        text: this.text.slice(startOffset, this.text.length)
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
    show(e) {
      e.preventDefault()
      this.showMenu = false
      this.x = e.clientX
      this.y = e.clientY
      this.$nextTick(() => {
        this.showMenu = true
      })
    },
    getSpanInfo() {
      let selection
      // Modern browsers.
      if (window.getSelection) {
        selection = window.getSelection()
      } else if (document.selection) {
        selection = document.selection
      }
      // If nothing is selected.
      if (selection.rangeCount <= 0) {
        return
      }
      const range = selection.getRangeAt(0)
      const preSelectionRange = range.cloneRange()
      preSelectionRange.selectNodeContents(this.$el)
      preSelectionRange.setEnd(range.startContainer, range.startOffset)
      const start = [...preSelectionRange.toString()].length
      const end = start + [...range.toString()].length
      return { start, end }
    },
    validateSpan(span, entities) {
      if (!span) {
        return false
      }
      if (span.start === span.end) {
        return false
      }
      for (const entity of this.entities) {
        if ((entity.start_offset <= span.start) && (span.start < entity.end_offset)) {
          return false
        }
        if ((entity.start_offset < span.end) && (span.end <= entity.end_offset)) {
          return false
        }
        if ((span.start < entity.start_offset) && (entity.end_offset < span.end)) {
          return false
        }
      }
      return true
    },
    open(e) {
      const span = this.getSpanInfo()
      const isValid = this.validateSpan(span, this.entities)
      if (isValid) {
        this.start = span.start
        this.end = span.end
        this.show(e)
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
