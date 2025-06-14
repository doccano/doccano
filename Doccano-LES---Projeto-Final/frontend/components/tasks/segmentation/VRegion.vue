<template>
  <v-group>
    <v-polygon
      :polygon="writablePolygon"
      :closed="true"
      :color="color"
      :draggable="true"
      :highlight-id="highlightId"
      :max-height="maxHeight"
      :max-width="maxWidth"
      :scale="scale"
      @click="$emit('click-polygon', writablePolygon)"
      @dragstart="onDragStart"
      @dragend="onDragEnd"
    />
    <v-circle
      ref="anchorRef"
      :config="{
        x: -10,
        y: -10,
        radius: 5,
        fill: 'white',
        stroke: 'black',
        scaleX: 1 / (scale || 1),
        scaleY: 1 / (scale || 1)
      }"
    />
    <template v-if="isSelected && !isMoving">
      <v-line
        v-for="(lineSegment, insertIndex) in writablePolygon.lineSegments"
        :key="insertIndex"
        :config="{
          draggable: false,
          hitStrokeWidth: 10,
          lineJoin: 'round',
          opacity: 1,
          points: lineSegment.points,
          stroke: 'transparent',
          strokeWidth: 5,
          strokeScaleEnabled: false
        }"
        @mousemove="onMouseMoveLine($event, lineSegment)"
        @mouseleave="hideAnchorPoint"
        @click="handleClickLine($event, writablePolygon, insertIndex + 1)"
      />
      <v-point
        v-for="(point, index) in writablePolygon.toPoints()"
        :key="`${writablePolygon.id}-${index}`"
        :color="index === selectedPoint ? color : 'white'"
        :point="point"
        :index="index"
        :max-width="maxWidth"
        :max-height="maxHeight"
        :scale="scale"
        @click="$emit('click-point', index)"
        @dragstart="hideAnchorPoint"
        @dragmove="handleDragMovePoint"
        @dragend="handleDragEndPoint"
        @dblclick="handleDoubleClickPoint"
      />
    </template>
  </v-group>
</template>

<script lang="ts">
import Vue from 'vue'
import Konva from 'konva'
import Flatten from '@flatten-js/core'
import VPolygon from './VPolygon.vue'
import VPoint from './VPoint.vue'
import Polygon from '@/domain/models/tasks/segmentation/Polygon'
import LineSegment from '@/domain/models/tasks/segmentation/LineSegment'
import { transform } from '@/domain/models/tasks/shared/Scaler'
import Point = Flatten.Point

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
    },
    highlightId: {
      type: String,
      default: ''
    },
    isSelected: {
      type: Boolean,
      default: false
    },
    selectedPoint: {
      type: Number,
      default: -1
    }
  },

  data() {
    return {
      isMoving: false,
      writablePolygon: this.polygon
    }
  },

  computed: {
    anchor() {
      return (this.$refs.anchorRef as Konva.ShapeConfig).getNode()
    }
  },

  watch: {
    polygon: {
      handler(newPolygon: Polygon) {
        this.writablePolygon = newPolygon
      },
      immediate: true,
      deep: true
    }
  },

  methods: {
    onDragStart() {
      this.isMoving = true
    },

    onDragEnd(polygon: Polygon, dx: number, dy: number) {
      this.isMoving = false
      this.$emit('drag-end-polygon', polygon, dx, dy)
    },

    handleDragMovePoint(index: number, x: number, y: number) {
      this.writablePolygon.movePoint(index, x, y)
      this.writablePolygon = this.writablePolygon.clone()
    },

    handleDragEndPoint(index: number, x: number, y: number) {
      this.$emit('drag-end-point', this.polygon, index, x, y)
    },

    handleDoubleClickPoint(index: number) {
      this.$emit('double-click-point', this.polygon, index)
    },

    onMouseMoveLine(e: Konva.KonvaEventObject<MouseEvent>, lineSegment: LineSegment) {
      const { offsetX, offsetY } = e.evt
      const { x: stageX = 0, y: stageY = 0 } = e.target.getStage()!.attrs
      const x = transform(offsetX, stageX, this.scale)
      const y = transform(offsetY, stageY, this.scale)
      const point = new Point(x, y)
      const closestPoint = lineSegment.getClosestPoint(point)
      this.showAnchorPoint(closestPoint.x, closestPoint.y)
    },

    handleClickLine(e: Konva.KonvaEventObject<MouseEvent>, polygon: Polygon, index: number) {
      const { offsetX, offsetY } = e.evt
      const { x: stageX = 0, y: stageY = 0 } = e.target.getStage()!.attrs
      const x = transform(offsetX, stageX, this.scale)
      const y = transform(offsetY, stageY, this.scale)
      this.hideAnchorPoint()
      this.$emit('click-line', polygon, index, x, y)
    },

    showAnchorPoint(x: number, y: number) {
      this.anchor.to({ x, y, duration: 0 })
      this.anchor.show()
    },

    hideAnchorPoint() {
      this.anchor.to({ x: -10, y: -10, duration: 0 })
      this.anchor.hide()
    }
  }
})
</script>
