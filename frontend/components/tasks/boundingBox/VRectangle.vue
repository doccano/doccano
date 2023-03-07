<template>
  <v-rect
    :config="{
      id: rect.id,
      x: rect.x,
      y: rect.y,
      width: rect.width,
      height: rect.height,
      opacity: 0.6,
      stroke: strokeColor,
      fill: color,
      strokeWidth,
      draggable: true,
      dragBoundFunc
    }"
    @dragstart="onDragStart"
    @dragend="onDragEnd"
    @transformend="$emit('transformend', $event)"
  />
</template>

<script lang="ts">
import Konva from 'konva'
import type { PropType } from 'vue'
import Vue from 'vue'
import { inverseTransform, transform } from '@/domain/models/tasks/shared/Scaler'
import Rectangle from '@/domain/models/tasks/boundingbox/Rectangle'

export default Vue.extend({
  props: {
    rect: {
      type: Object as PropType<Rectangle>,
      required: true
    },
    color: {
      type: String,
      default: '#00FF00'
    },
    draggable: {
      type: Boolean,
      default: true
    },
    highlightId: {
      type: String,
      default: 'uuid'
    },
    opacity: {
      type: Number,
      default: 0.6
    },
    scale: {
      type: Number,
      required: true
    },
    maxWidth: {
      type: Number,
      required: true
    },
    maxHeight: {
      type: Number,
      required: true
    }
  },

  data() {
    return {
      stageX: 0,
      stageY: 0,
      originX: 0,
      originY: 0
    }
  },

  computed: {
    strokeColor() {
      return this.rect.id === this.highlightId ? '#ff0000' : `${this.color}CC`
    },

    strokeWidth() {
      return this.rect.id === this.highlightId ? 5 : 1
    }
  },

  methods: {
    dragBoundFunc(pos: { x: number; y: number }) {
      const [minX, minY, maxX, maxY] = this.rect.minMaxPoints()
      let x = transform(pos.x, this.stageX, this.scale)
      let y = transform(pos.y, this.stageY, this.scale)
      x -= this.originX
      y -= this.originY
      if (minY + y < 0) y = -minY
      if (minX + x < 0) x = -minX
      if (maxY + y > this.maxHeight) y = this.maxHeight - maxY
      if (maxX + x > this.maxWidth) x = this.maxWidth - maxX
      x += this.originX
      y += this.originY
      x = inverseTransform(x, this.stageX, this.scale)
      y = inverseTransform(y, this.stageY, this.scale)
      return { x, y }
    },

    onDragStart(e: Konva.KonvaEventObject<DragEvent>) {
      this.originX = e.target.attrs.x
      this.originY = e.target.attrs.y
      const { x = 0, y = 0 } = e.target.getStage()!.attrs
      this.stageX = x
      this.stageY = y
    },

    onDragEnd(e: Konva.KonvaEventObject<DragEvent>) {
      const { x, y } = e.target.attrs
      const newRect = this.rect.transform(x, y, this.rect.width, this.rect.height)
      this.$emit('dragend', newRect)
    }
  }
})
</script>
