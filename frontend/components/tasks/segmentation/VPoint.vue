<template>
  <v-circle
    :config="{
      x: point.x,
      y: point.y,
      radius: 5,
      fill: color,
      stroke: 'black',
      draggable: true,
      scaleX: 1 / (scale || 1),
      scaleY: 1 / (scale || 1),
      dragBoundFunc
    }"
    v-on="
      index === 0
        ? {
            hitStrokeWidth: 12,
            mouseover: onMouseOverStartPoint,
            mouseout: onMouseOutStartPoint
          }
        : {}
    "
    @click="onClick"
    @dblclick="onDoubleClick"
    @dragstart="onDragStart"
    @dragmove="onDragMove"
    @dragend="onDragEnd"
    @mouseenter="onMouseEnter"
    @mouseleave="onMouseLeave"
  />
</template>

<script lang="ts">
import Vue from 'vue'
import Konva from 'konva'
import Flatten from '@flatten-js/core'
import { transform, inverseTransform } from '@/domain/models/tasks/shared/Scaler'
import Point = Flatten.Point

export default Vue.extend({
  props: {
    color: {
      type: String,
      default: '#00FF00'
    },
    point: {
      type: Point,
      required: true
    },
    index: {
      type: Number,
      required: true
    },
    maxWidth: {
      type: Number,
      default: 0
    },
    maxHeight: {
      type: Number,
      default: 0
    },
    scale: {
      type: Number,
      default: 1
    }
  },

  data() {
    return {
      stageX: 0,
      stageY: 0
    }
  },

  methods: {
    dragBoundFunc(pos: { x: number; y: number }) {
      let x = transform(pos.x, this.stageX, this.scale)
      let y = transform(pos.y, this.stageY, this.scale)
      if (x < 0) x = 0
      if (y < 0) y = 0
      if (x > this.maxWidth) x = this.maxWidth
      if (y > this.maxHeight) y = this.maxHeight
      x = inverseTransform(x, this.stageX, this.scale)
      y = inverseTransform(y, this.stageY, this.scale)
      return { x, y }
    },

    onClick() {
      this.$emit('click', this.index)
    },

    onDoubleClick() {
      this.$emit('dblclick', this.index)
    },

    onDragStart(e: Konva.KonvaEventObject<DragEvent>) {
      const { x = 0, y = 0 } = e.target.getStage()!.attrs
      this.stageX = x
      this.stageY = y
      this.$emit('dragstart', this.index)
    },

    onDragMove(e: Konva.KonvaEventObject<DragEvent>) {
      const { x, y } = e.target.attrs
      this.$emit('dragmove', this.index, x, y)
    },

    onDragEnd(e: Konva.KonvaEventObject<DragEvent>) {
      const { x, y } = e.target.attrs
      this.$emit('dragend', this.index, x, y)
    },

    onMouseEnter(e: Konva.KonvaEventObject<MouseEvent>) {
      e.target.getStage()!.container().style.cursor = 'crosshair'
    },

    onMouseLeave(e: Konva.KonvaEventObject<MouseEvent>) {
      e.target.getStage()!.container().style.cursor = 'default'
    },

    onMouseOverStartPoint(e: Konva.KonvaEventObject<MouseEvent>) {
      e.target.scale({ x: 2 / this.scale, y: 2 / this.scale })
      this.$emit('mouseover')
    },

    onMouseOutStartPoint(e: Konva.KonvaEventObject<MouseEvent>) {
      e.target.scale({ x: 1 / this.scale, y: 1 / this.scale })
      this.$emit('mouseout')
    }
  }
})
</script>
