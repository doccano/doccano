<template>
  <v-line
    :config="{
      id: polygon.id,
      points: polygon.flattenedPoints,
      closed: closed,
      draggable: true,
      opacity: 0.6,
      stroke: strokeColor,
      strokeWidth,
      fill: color,
      dragBoundFunc
    }"
    @click="click"
    @dragstart="onDragStart"
    @dragend="onDragEnd"
    @mouseenter="mouseEnter"
    @mouseleave="mouseLeave"
  />
</template>

<script lang="ts">
import Vue from 'vue'
import Konva from 'konva'
import Polygon from '@/domain/models/tasks/segmentation/Polygon'
import { transform, inverseTransform } from '@/domain/models/tasks/shared/Scaler'

export default Vue.extend({
  props: {
    polygon: {
      type: Polygon,
      required: true
    },
    color: {
      type: String,
      default: '#00FF00'
    },
    closed: {
      type: Boolean,
      default: false
    },
    draggable: {
      type: Boolean,
      default: false
    },
    opacity: {
      type: Number,
      default: 0.6
    },
    scale: {
      type: Number,
      default: 1
    },
    maxWidth: {
      type: Number,
      default: 0
    },
    maxHeight: {
      type: Number,
      default: 0
    },
    highlightId: {
      type: String,
      required: false,
      default: 'uuid'
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
      return this.polygon.id === this.highlightId ? '#ff0000' : `${this.color}CC`
    },

    strokeWidth() {
      return this.polygon.id === this.highlightId ? 5 : 1
    }
  },

  methods: {
    onDragStart(e: Konva.KonvaEventObject<DragEvent>) {
      this.originX = e.target.x()
      this.originY = e.target.y()
      const { x = 0, y = 0 } = e.target.getStage()!.attrs
      this.stageX = x
      this.stageY = y
      this.$emit('dragstart')
    },

    dragBoundFunc(pos: { x: number; y: number }) {
      let x = transform(pos.x, this.stageX, this.scale)
      let y = transform(pos.y, this.stageY, this.scale)
      const [minX, minY, maxX, maxY] = this.polygon.minMaxPoints()
      if (minY + y < 0) y = -1 * minY
      if (minX + x < 0) x = -1 * minX
      if (maxY + y > this.maxHeight) y = this.maxHeight - maxY
      if (maxX + x > this.maxWidth) x = this.maxWidth - maxX
      x = inverseTransform(x, this.stageX, this.scale)
      y = inverseTransform(y, this.stageY, this.scale)
      return { x, y }
    },

    onDragEnd(e: Konva.KonvaEventObject<DragEvent>) {
      const dx = e.target.x() - this.originX
      const dy = e.target.y() - this.originY
      e.target.move({ x: -dx, y: -dy })
      this.$emit('dragend', this.polygon, dx, dy)
    },

    click(id: string) {
      this.$emit('click', id)
    },

    mouseEnter(e: Konva.KonvaEventObject<MouseEvent>) {
      e.target.getStage()!.container().style.cursor = 'pointer'
    },

    mouseLeave(e: Konva.KonvaEventObject<MouseEvent>) {
      e.target.getStage()!.container().style.cursor = 'default'
    }
  }
})
</script>
