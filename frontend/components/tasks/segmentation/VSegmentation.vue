<template>
  <v-stage ref="stageRef" :config="{ ...configStage, dragBoundFunc }" @mousedown="onMouseDown">
    <v-layer>
      <base-image :image-url="imageUrl" @loaded="imageLoaded" />
    </v-layer>
    <v-layer>
      <v-editing-region
        v-if="!!editingPolygon"
        :polygon="editingPolygon"
        :color="editingPolygon.getColor(labels)"
        :max-width="imageSize.width"
        :max-height="imageSize.height"
        :scale="scale"
        @drag-end-polygon="translatePolygon"
        @mouse-over-start-point="onMouseOverStartPoint"
        @mouse-out-start-point="onMouseOutStartPoint"
        @drag-point="movePoint"
        @double-click-point="removePoint"
      />
    </v-layer>
    <v-layer>
      <v-region
        v-for="(polygon, index) in readonlyPolygons"
        :key="`polygon-${index}`"
        :polygon="polygon"
        :highlight-id="highlightId"
        :is-selected="polygon.id === selectedPolygon"
        :selected-point="selectedPoint"
        :max-width="imageSize.width"
        :max-height="imageSize.height"
        :scale="scale"
        :color="polygon.getColor(labels)"
        @click-point="updateSelectedPoint"
        @click-line="insertPoint"
        @click-polygon="updateSelectedPolygon"
        @drag-end-polygon="translatePolygon"
        @drag-end-point="movePoint"
        @double-click-point="removePoint"
      />
    </v-layer>
  </v-stage>
</template>

<script lang="ts">
import Konva from 'konva'
import type { PropType } from 'vue'
import Vue from 'vue'
import VEditingRegion from './VEditingRegion.vue'
import VRegion from './VRegion.vue'
import BaseImage from '@/components/tasks/image/BaseImage.vue'
import Polygon from '@/domain/models/tasks/segmentation/Polygon'
import PolygonProps from '@/domain/models/tasks/segmentation/PolygonProps'
import LabelProps from '@/domain/models/tasks/shared/LabelProps'
import { transform } from '@/domain/models/tasks/shared/Scaler'

export default Vue.extend({
  name: 'VSegmentation',

  components: {
    VEditingRegion,
    VRegion,
    BaseImage
  },

  props: {
    imageUrl: {
      type: String,
      required: true
    },
    labels: {
      type: Array as () => LabelProps[],
      required: true
    },
    polygons: {
      type: Array as () => PolygonProps[],
      required: true
    },
    selectedLabel: {
      type: Object as PropType<LabelProps | undefined>,
      default: undefined
    },
    scale: {
      type: Number,
      default: 1
    },
    highlightId: {
      type: String,
      required: false,
      default: 'uuid'
    }
  },

  data() {
    return {
      imageSize: {
        width: 0,
        height: 0
      },
      editingPolygon: null as Polygon | null,
      isMouseOverStartPoint: false,
      selectedPolygon: null as string | null,
      selectedPoint: -1,
      configStage: {
        width: window.innerWidth,
        height: window.innerHeight,
        draggable: true
      },
      stage: {} as Konva.Stage
    }
  },

  computed: {
    readonlyPolygons() {
      return this.polygons.map((p: PolygonProps) => new Polygon(p.label, p.points, p.id))
    }
  },

  watch: {
    scale() {
      this.setZoom()
    }
  },

  mounted() {
    document.addEventListener('keydown', this.removePointOrPolygon)
    window.addEventListener('resize', this.setZoom)
    this.stage = (this.$refs.stageRef as unknown as Konva.StageConfig).getNode()
  },

  beforeDestroy() {
    document.removeEventListener('keydown', this.removePointOrPolygon)
    window.removeEventListener('resize', this.setZoom)
  },

  methods: {
    onMouseDown(e: Konva.KonvaEventObject<MouseEvent>) {
      if (e.target instanceof Konva.Image) {
        // while new polygon is creating, prevent to select polygon.
        this.selectedPolygon = null
      }
      if (!this.selectedLabel) {
        return
      }
      // prevent multiple event.
      if (e.target instanceof HTMLCanvasElement) {
        return
      }
      // prevent to create circle on Polygon.
      if (e.target instanceof Konva.Line) {
        return
      }
      if (e.target instanceof Konva.Circle) {
        if (
          this.isMouseOverStartPoint &&
          this.editingPolygon &&
          this.editingPolygon.canBeClosed()
        ) {
          this.$emit('add-polygon', this.editingPolygon.toProps())
          this.editingPolygon = null
        }
        return
      }

      const pos = this.stage.getPointerPosition()!
      const { x: stageX = 0, y: stageY = 0 } = this.stage.attrs
      pos.x = transform(pos.x, stageX, this.scale)
      pos.y = transform(pos.y, stageY, this.scale)
      if (!this.editingPolygon) {
        this.editingPolygon = new Polygon(this.selectedLabel.id, [pos.x, pos.y])
      } else {
        this.editingPolygon.addPoint(pos.x, pos.y)
      }
    },

    onMouseOverStartPoint() {
      this.isMouseOverStartPoint = true
    },

    onMouseOutStartPoint() {
      this.isMouseOverStartPoint = false
    },

    updateSelectedPolygon(polygon: Polygon) {
      this.selectedPoint = -1
      if (this.selectedPolygon === polygon.id) {
        this.selectedPolygon = null
      } else {
        this.selectedPolygon = polygon.id
      }
      this.$emit('select-polygon', this.selectedPolygon)
    },

    updateSelectedPoint(point: number) {
      if (this.selectedPoint === point) {
        this.selectedPoint = -1
      } else {
        this.selectedPoint = point
      }
    },

    insertPoint(polygon: Polygon, index: number, x: number, y: number) {
      polygon.insertPoint(x, y, index)
      this.$emit('update-polygon', polygon.toProps())
    },

    translatePolygon(polygon: Polygon, dx: number, dy: number) {
      polygon.translate(dx, dy)
      this.$emit('update-polygon', polygon.toProps())
    },

    movePoint(polygon: Polygon, index: number, x: number, y: number) {
      polygon.movePoint(index, x, y)
      this.$emit('update-polygon', polygon.toProps())
    },

    removePoint(polygon: Polygon, index: number) {
      polygon.removePoint(index)
      this.$emit('update-polygon', polygon.toProps())
    },

    removePointOrPolygon(e: KeyboardEvent) {
      if (e.key === 'Backspace' || e.key === 'Delete') {
        if (this.selectedPoint !== -1) {
          const polygon = this.readonlyPolygons.find((p) => p.id === this.selectedPolygon)
          this.removePoint(polygon!, this.selectedPoint)
          this.selectedPoint = -1
          return
        }
        if (this.selectedPolygon !== null) {
          this.$emit('delete-polygon', this.selectedPolygon)
          this.selectedPolygon = null
        }
      }
    },

    dragBoundFunc(pos: { x: number; y: number }) {
      const { stageX = 0, stageY = 0 } = this.stage.attrs
      let x = pos.x - stageX
      let y = pos.y - stageY
      const paddingX = this.imageSize.width * this.scale - this.configStage.width
      const paddingY = this.imageSize.height * this.scale - this.configStage.height
      if (paddingX + x < 0) x = -paddingX
      if (paddingY + y < 0) y = -paddingY
      if (this.configStage.width + paddingX + x > this.imageSize.width * this.scale) x = 0
      if (this.configStage.height + paddingY + y > this.imageSize.height * this.scale) y = 0
      x += stageX
      y += stageY
      return { x, y }
    },

    imageLoaded(width: number, height: number) {
      const maxScale = this.$el.clientWidth / width
      const imageIsSmallerThanContainer = maxScale > 1
      this.imageSize.width = width
      this.imageSize.height = height
      if (imageIsSmallerThanContainer) {
        this.configStage.width = width
        this.configStage.height = height
        this.stage.scale({ x: 1, y: 1 })
        this.$emit('update-scale', 1)
      } else {
        this.configStage.width = width * maxScale
        this.configStage.height = height * maxScale
        this.stage.scale({ x: maxScale, y: maxScale })
        this.$emit('update-scale', maxScale)
      }
      this.stage.draw()
    },

    setZoom() {
      if (this.scale < 0) {
        return
      }
      const maxScale = this.$el.clientWidth / this.imageSize.width
      this.stage.scale({ x: this.scale, y: this.scale })
      if (this.scale <= maxScale) {
        this.configStage.width = this.imageSize.width * this.scale
      } else {
        this.configStage.width = this.imageSize.width * maxScale
      }
      this.configStage.height = this.imageSize.height * this.scale
      this.$el.setAttribute('style', `min-height: ${this.configStage.height}px`)
    }
  }
})
</script>
