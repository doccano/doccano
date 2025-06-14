<template>
  <v-group>
    <v-polygon
      :polygon="polygon"
      :closed="false"
      :color="color"
      :draggable="true"
      :max-height="maxHeight"
      :max-width="maxWidth"
      :scale="scale"
      @dragend="onDragEnd"
    />
    <v-point
      v-for="(point, index) in polygon.toPoints()"
      :key="index"
      color="white"
      :point="point"
      :index="index"
      :max-width="maxWidth"
      :max-height="maxHeight"
      :scale="scale"
      @mouseover="onMouseOverStartPoint"
      @mouseout="onMouseOutStartPoint"
      @dragmove="handleDragMovePoint"
      @dblclick="handleDoubleClickPoint"
    />
  </v-group>
</template>

<script lang="ts">
import Vue from 'vue'
import VPolygon from './VPolygon.vue'
import VPoint from './VPoint.vue'
import Polygon from '@/domain/models/tasks/segmentation/Polygon'

export default Vue.extend({
  components: {
    VPolygon,
    VPoint
  },

  props: {
    polygon: {
      type: Polygon,
      required: true
    },
    color: {
      type: String,
      default: '#00FF00'
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

  methods: {
    onDragEnd(polygon: Polygon, dx: number, dy: number) {
      this.$emit('drag-end-polygon', polygon, dx, dy)
    },

    onMouseOverStartPoint() {
      if (!this.polygon.canBeClosed()) return
      this.$emit('mouse-over-start-point')
    },

    onMouseOutStartPoint() {
      this.$emit('mouse-out-start-point')
    },

    handleDragMovePoint(index: number, x: number, y: number) {
      this.$emit('drag-point', this.polygon, index, x, y)
    },

    handleDoubleClickPoint(index: number) {
      this.$emit('double-click-point', this.polygon, index)
    }
  }
})
</script>
