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
          @deleteLink="deleteLink($event.id, $event.ndx)"
          @selectNewLinkType="selectNewLinkType($event)"
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
      default: () => {
      },
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
          links: entity.links ? entity.links.map(link => {
            return {
              id: link.id,
              type: link.type,
              color: this.getColor(link.type),
              targetId: link.annotation_id_2,
              targetLabel: null // target label can be computed only after all chunks are made, see line 204
            }
          }) : null
        })
      }
      // add the rest of text.
      chunks = chunks.concat(this.makeChunks(characters.slice(startOffset, characters.length).join('')));

      // populate the links. Must be done after chunk creation
      chunks.forEach(chunk => {
        if (chunk.links) {
          chunk.links.forEach(link => {
            link.targetLabel = chunks.find(target => target.id === link.targetId).text;
          });
        }
      });

      return chunks;
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

      const topPoints = this.drawnCountPoints(this.chunks.length);
      const bottomPoints = this.drawnCountPoints(this.chunks.length);

      const chunks = this.chunks;

      chunks.forEach(function(sourceChunk, sourceNdx) {
        if (sourceChunk.links) {
          sourceChunk.links.forEach(function(link) {
            let childPos = document.getElementById('spn-' + sourceChunk.id).getBoundingClientRect();
            const y1 = childPos.y - parentPos.y;

            childPos = document.getElementById('spn-' + link.targetId).getBoundingClientRect();
            const y2 = childPos.y - parentPos.y;

            const targetNdx = chunks.findIndex(ch => ch.id === link.targetId);

            if (y1 < y2) {
              bottomPoints[sourceNdx].count++;
              topPoints[targetNdx].count++;

            } else if (y1 > y2) {
              topPoints[sourceNdx].count++;
              bottomPoints[targetNdx].count++;

            } else {
              bottomPoints[sourceNdx].count++;
              bottomPoints[targetNdx].count++;
            }
          });
        }
      });

      chunks.forEach(function(sourceChunk, sourceNdx) {
        if (sourceChunk.links) {
          sourceChunk.links.forEach(function(link) {
            const sourcePos = document.getElementById('spn-' + sourceChunk.id).getBoundingClientRect();
            let x1 = sourcePos.x - parentPos.x;
            let y1 = sourcePos.y - parentPos.y;

            const targetPos = document.getElementById('spn-' + link.targetId).getBoundingClientRect();
            let x2 = targetPos.x - parentPos.x;
            let y2 = targetPos.y - parentPos.y;

            const targetNdx = chunks.findIndex(ch => ch.id === link.targetId);

            ctx.beginPath();
            ctx.lineWidth = 3;
            ctx.strokeStyle = link.color;

            if (y1 < y2) {
              bottomPoints[sourceNdx].drawn++;
              topPoints[targetNdx].drawn++;

              x1 += bottomPoints[sourceNdx].drawn * sourcePos.width / (bottomPoints[sourceNdx].count + 1);
              y1 += sourcePos.height;

              x2 += topPoints[targetNdx].drawn * targetPos.width / (topPoints[targetNdx].count + 1);

              ctx.moveTo(x1, y1);
              ctx.lineTo(x1, y1 + 12);
              ctx.lineTo(x2, y2 - 12);
              ctx.lineTo(x2, y2);
              ctx.stroke();

              ctx.fillStyle = link.color;
              ctx.beginPath();
              ctx.moveTo(x2, y2);
              ctx.lineTo(x2 - 3, y2 - 5);
              ctx.lineTo(x2 + 3, y2 - 5);
              ctx.lineTo(x2, y2);
              ctx.closePath();
              ctx.stroke();

            } else if (y1 > y2) {
              topPoints[sourceNdx].drawn++;
              bottomPoints[targetNdx].drawn++;

              x1 += topPoints[sourceNdx].drawn * sourcePos.width / (topPoints[sourceNdx].count + 1);

              x2 += bottomPoints[targetNdx].drawn * targetPos.width / (bottomPoints[targetNdx].count + 1);
              y2 += targetPos.height;

              ctx.moveTo(x1, y1);
              ctx.lineTo(x1, y1 - 12);
              ctx.lineTo(x2, y2 + 12);
              ctx.lineTo(x2, y2);
              ctx.stroke();

              ctx.fillStyle = link.color;
              ctx.beginPath();
              ctx.moveTo(x2, y2);
              ctx.lineTo(x2 - 3, y2 + 5);
              ctx.lineTo(x2 + 3, y2 + 5);
              ctx.lineTo(x2, y2);
              ctx.closePath();
              ctx.stroke();

            } else {
              bottomPoints[sourceNdx].drawn++;
              bottomPoints[targetNdx].drawn++;

              x1 += bottomPoints[sourceNdx].drawn * sourcePos.width / (bottomPoints[sourceNdx].count + 1);
              y1 += sourcePos.height;

              x2 += bottomPoints[targetNdx].drawn * targetPos.width / (bottomPoints[targetNdx].count + 1);
              y2 += targetPos.height;

              ctx.moveTo(x1, y1);
              ctx.lineTo(x1, y1 + 12);
              ctx.lineTo(x2, y2 + 12);
              ctx.lineTo(x2, y2);
              ctx.stroke();

              ctx.fillStyle = link.color;
              ctx.beginPath();
              ctx.moveTo(x2, y2);
              ctx.lineTo(x2 - 3, y2 + 5);
              ctx.lineTo(x2 + 3, y2 + 5);
              ctx.lineTo(x2, y2);
              ctx.closePath();
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
    },

    getColor(typeId) {
      const type = this.linkTypes.find(type => type.id === typeId);
      if (type) {
        return type.color;
      }
      return "#787878";
    },

    drawnCountPoints(size) {
      const points = Array(size);

      for (let i = 0; i < points.length; i++) {
        points[i] = {
          drawn: 0,
          count: 0
        }
      }

      return points;
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
