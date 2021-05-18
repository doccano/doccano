<template>
  <div id="connections-wrapper">
    <div class="highlight-container highlight-container--bottom-labels" @click="open" @touchend="open">
      <entity-item
          v-for="(chunk, i) in chunks"
          :key="i"
          :spanid="chunk.id"
          :content="chunk.text"
          :newline="chunk.newline"
          :label="chunk.label"
          :color="chunk.color"
          :labels="labels"
          :link-types="linkTypes"
          :source-chunk="sourceChunk"
          :source-link-type="sourceLinkType"
          @remove="deleteAnnotation(chunk.id)"
          @update="updateEntity($event.id, chunk.id)"
          @selectSource="selectSource(chunk)"
          @selectTarget="selectTarget(chunk)"
          @selectLink="selectLink($event)"
          @deleteLink="deleteLink($event.id, $event.ndx)"
          @selectNewLinkType="selectNewLinkType($event)"
          @changeLinkType="changeLinkType($event)"
          @hideAllLinkMenus="hideAllLinkMenus()"
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
              v-shortkey="[label.suffixKey]"
              @shortkey="assignLabel(label.id)"
              @click="assignLabel(label.id)"
          >
            <v-list-item-content>
              <v-list-item-title v-text="label.text"/>
            </v-list-item-content>
            <v-list-item-action>
              <v-list-item-action-text v-text="label.suffixKey"/>
            </v-list-item-action>
          </v-list-item>
        </v-list>
      </v-menu>
    </div>

    <canvas id="connections">
    </canvas>
  </div>
</template>

<script>
import EntityItem from './EntityItem'

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
    linkTypes: {
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
    },
    sourceChunk: {
      type: Object,
      default: () => {
      },
      required: true
    },
    sourceLinkType: {
      type: Object,
      default: () => {},
      required: true
    },
    selectSource: {
      type: Function,
      default: () => ([]),
      required: true
    },
    selectTarget: {
      type: Function,
      default: () => ([]),
      required: true
    },
    selectLink: {
      type: Function,
      default: () => ([]),
      required: true
    },
    deleteLink: {
      type: Function,
      default: () => ([]),
      required: true
    },
    selectNewLinkType: {
      type: Function,
      default: () => ([]),
      required: true
    },
    changeLinkType: {
      type: Function,
      default: () => ([]),
      required: true
    },
    hideAllLinkMenus: {
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
      return this.entities.slice().sort((a, b) => a.startOffset - b.startOffset)
    },
    chunks() {
      let chunks = []
      let startOffset = 0
      // to count the number of characters correctly.
      const characters = [...this.text]
      for (const entity of this.sortedEntities) {
        // add non-entities to chunks.
        let piece = characters.slice(startOffset, entity.startOffset).join('')
        chunks = chunks.concat(this.makeChunks(piece))
        startOffset = entity.endOffset
        // add entities to chunks.
        const label = this.labelObject[entity.label]
        piece = characters.slice(entity.startOffset, entity.endOffset).join('')
        chunks.push({
          id: entity.id,
          label: label.text,
          color: label.backgroundColor,
          text: piece,
          selectedAsLinkSource: false,
          links: [] // must use targetId to get target label (it's not stored)
        })
      }
      // add the rest of text.
      chunks = chunks.concat(this.makeChunks(characters.slice(startOffset, characters.length).join('')))
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

  updated() {
    this.$nextTick(() => {
      const parentPos = document.getElementById('connections-wrapper').getBoundingClientRect();
      const canvas = document.getElementById('connections');
      canvas.width = parentPos.width;
      canvas.height = parentPos.height;
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, parentPos.width, parentPos.height);

      this.chunks.forEach(function(fromChunk) {
        if (fromChunk.links) {
          fromChunk.links.forEach(function(link) {
            let childPos = document.getElementById('spn-' + fromChunk.id).getBoundingClientRect();
            const x1 = (childPos.x + childPos.width / 2) - parentPos.x;
            const y1 = (childPos.y + childPos.height / 2) - parentPos.y;

            childPos = document.getElementById('spn-' + link.targetId).getBoundingClientRect();
            const x2 = (childPos.x + childPos.width / 2) - parentPos.x;
            const y2 = (childPos.y + childPos.height / 2) - parentPos.y;

            ctx.beginPath();
            ctx.lineWidth = 3;
            ctx.moveTo(x1, y1);
            ctx.strokeStyle = link.color;

            if (y1 === y2) {
              ctx.lineTo(x1, y1 + 35);
              ctx.stroke();

              ctx.lineTo(x2, y1 + 35);
              ctx.stroke();

              ctx.lineTo(x2, y2);
              ctx.stroke();

            } else {
              ctx.lineTo(x2, y2);
              ctx.stroke();
            }
          });
        }
      });
    });
  },

  methods: {
    makeChunks(text) {
      const chunks = []
      const snippets = text.split('\n')
      for (const snippet of snippets.slice(0, -1)) {
        chunks.push({
          label: null,
          color: null,
          text: snippet + '\n',
          newline: false
        })
        chunks.push({
          label: null,
          color: null,
          text: '',
          newline: true
        })
      }
      chunks.push({
        label: null,
        color: null,
        text: snippets.slice(-1)[0],
        newline: false
      })
      return chunks
    },

    show(e) {
      e.preventDefault()
      this.showMenu = false
      this.x = e.clientX || e.changedTouches[0].clientX
      this.y = e.clientY || e.changedTouches[0].clientY
      this.$nextTick(() => {
        this.showMenu = true
      })
    },

    setSpanInfo() {
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
      this.start = [...preSelectionRange.toString()].length
      this.end = this.start + [...range.toString()].length
    },

    validateSpan() {
      if ((typeof this.start === 'undefined') || (typeof this.end === 'undefined')) {
        return false
      }
      if (this.start === this.end) {
        return false
      }
      for (const entity of this.entities) {
        if ((entity.startOffset <= this.start) && (this.start < entity.endOffset)) {
          return false
        }
        if ((entity.startOffset < this.end) && (this.end <= entity.endOffset)) {
          return false
        }
        if ((this.start < entity.startOffset) && (entity.endOffset < this.end)) {
          return false
        }
      }
      return true
    },

    open(e) {
      this.$emit('hideAllLinkMenus');

      this.setSpanInfo()
      if (this.validateSpan()) {
        this.show(e)
      }
    },

    assignLabel(labelId) {
      if (this.validateSpan()) {
        this.addEntity(this.start, this.end, labelId)
        this.showMenu = false
        this.start = 0
        this.end = 0
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
  line-height: 70px !important;
  display: flex;
  flex-wrap: wrap;
  white-space: pre-wrap;
  cursor: default;
  position: relative;
  z-index: 1;
}

.highlight-container.highlight-container--bottom-labels .highlight.bottom {
  margin-top: 6px;
}

#connections-wrapper {
  position: relative;
}

#connections-wrapper canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}
</style>
