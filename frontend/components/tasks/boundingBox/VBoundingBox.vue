<template>
  <v-stage
    ref="stageRef"
    :config="{ ...configStage, dragBoundFunc }"
    @mousedown="onMouseDown"
    @mouseup="onMouseUp"
    @mousemove="onMouseMove"
  >
    <v-layer>
      <base-image :image-url="imageUrl" @loaded="imageLoaded" />
    </v-layer>
    <v-layer>
      <v-rectangle
        v-for="rect in annotationsToDraw"
        :key="rect.id"
        :rect="rect"
        :color="rect.getColor(labels)"
        :highlight-id="highlightId"
        :max-width="imageSize.width"
        :max-height="imageSize.height"
        :scale="scale"
        @dragend="onDragEnd"
        @transformend="handleTransformEnd"
      />
      <v-transformer
        ref="transformerRef"
        :config="{
          rotateEnabled: false,
          flipEnabled: false,
          keepRatio: false,
          boundBoxFunc
        }"
      />
    </v-layer>
  </v-stage>
</template>

<script lang="ts">
import Konva from 'konva'
import { Box } from 'konva/lib/shapes/Transformer.d'
import type { PropType } from 'vue'
import Vue from 'vue'
import VRectangle from './VRectangle.vue'
import BaseImage from '@/components/tasks/image/BaseImage.vue'
import Rectangle from '@/domain/models/tasks/boundingbox/Rectangle'
import RectangleProps from '@/domain/models/tasks/boundingbox/RectangleProps'
import LabelProps from '@/domain/models/tasks/shared/LabelProps'
import { inverseTransform, transform } from '@/domain/models/tasks/shared/Scaler'

export default Vue.extend({
  name: 'VBoundingBox',

  components: {
    BaseImage,
    VRectangle
  },

  props: {
    imageUrl: {
      type: String,
      required: true
    },
    labels: {
      type: Array as PropType<LabelProps[]>,
      required: true
    },
    rectangles: {
      type: Array as PropType<RectangleProps[]>,
      required: true
    },
    selectedLabel: {
      type: Object as PropType<LabelProps | undefined>,
      default: undefined
    },
    scale: {
      type: Number,
      required: true
    },
    highlightId: {
      type: String,
      required: false,
      default: 'uuid'
    }
  },

  data() {
    return {
      selectedRectangle: null as string | null,
      newRectangle: null as Rectangle | null,
      imageSize: {
        width: 0,
        height: 0
      },
      configStage: {
        width: window.innerWidth,
        height: window.innerHeight,
        draggable: true
      },
      stage: {} as Konva.Stage
    }
  },

  computed: {
    annotations(): Rectangle[] {
      return this.rectangles.map((r) => new Rectangle(r.label, r.x, r.y, r.width, r.height, r.id))
    },

    transformer(): Konva.Transformer {
      return (this.$refs.transformerRef as unknown as Konva.TransformerConfig).getNode()
    },

    annotationsToDraw(): Rectangle[] {
      if (this.newRectangle) {
        return this.annotations.concat(this.newRectangle)
      }
      return this.annotations
    }
  },

  watch: {
    scale() {
      this.setZoom()
    },

    imageUrl() {
      this.selectedRectangle = null
      this.updateTransformer()
    }
  },

  mounted() {
    document.addEventListener('keydown', this.removeRectangle)
    window.addEventListener('resize', this.setZoom)
    this.stage = (this.$refs.stageRef as unknown as Konva.StageConfig).getNode()
  },

  beforeDestroy() {
    document.removeEventListener('keydown', this.removeRectangle)
    window.removeEventListener('resize', this.setZoom)
  },

  methods: {
    updateTransformer() {
      // here we need to manually attach or detach Transformer node
      const selectedNode = this.stage.findOne(`#${this.selectedRectangle}`)
      // do nothing if selected node is already attached
      if (selectedNode === this.transformer.getNode()) {
        return
      }

      if (selectedNode) {
        // attach to another node
        this.transformer.nodes([selectedNode])
      } else {
        // remove transformer
        this.transformer.nodes([])
      }
      this.$emit('select-rectangle', this.selectedRectangle)
    },

    boundBoxFunc(_: Box, newBoundBox: Box) {
      const box = { ...newBoundBox }
      const { x: stageX = 0, y: stageY = 0 } = this.stage.attrs
      box.x = transform(box.x, stageX, this.scale)
      box.y = transform(box.y, stageY, this.scale)
      box.width = transform(box.width, 0, this.scale)
      box.height = transform(box.height, 0, this.scale)
      if (box.x < 0) {
        box.width += box.x
        box.x = 0
      }
      if (box.y < 0) {
        box.height += box.y
        box.y = 0
      }
      if (box.x + box.width > this.imageSize.width) box.width = this.imageSize.width - box.x
      if (box.y + box.height > this.imageSize.height) box.height = this.imageSize.height - box.y
      box.x = inverseTransform(box.x, stageX, this.scale)
      box.y = inverseTransform(box.y, stageY, this.scale)
      box.width = inverseTransform(box.width, 0, this.scale)
      box.height = inverseTransform(box.height, 0, this.scale)
      return box
    },

    onMouseDown(e: Konva.KonvaEventObject<MouseEvent>) {
      if (e.target instanceof Konva.Image) {
        // while new polygon is creating, prevent to select polygon.
        const clickedOutsideOfRectangle = !!this.selectedRectangle
        this.selectedRectangle = null
        this.updateTransformer()
        if (clickedOutsideOfRectangle) {
          return
        }
      }
      // prevent multiple event.
      if (e.target instanceof HTMLCanvasElement) {
        return
      }

      // clicked on transformer - do nothing
      const clickedOnTransformer = e.target.getParent().className === 'Transformer'
      if (clickedOnTransformer) {
        return
      }

      // prevent to create circle on Polygon.
      if (e.target instanceof Konva.Rect) {
        const rectId = e.target.id()
        const rect = this.annotations.find((r) => r.id === rectId)
        if (rect && !this.selectedRectangle) {
          this.selectedRectangle = rectId
        } else {
          this.selectedRectangle = null
        }
        this.updateTransformer()
        return
      }

      if (!this.newRectangle && !!this.selectedLabel) {
        this.configStage.draggable = false
        const pos = this.stage.getPointerPosition()!
        const { x: stageX = 0, y: stageY = 0 } = this.stage.attrs
        pos.x = transform(pos.x, stageX, this.scale)
        pos.y = transform(pos.y, stageY, this.scale)
        this.newRectangle = new Rectangle(this.selectedLabel.id, pos.x, pos.y, 0, 0)
      }
    },

    onMouseUp() {
      if (this.newRectangle && this.newRectangle.exists()) {
        const pos = this.stage.getPointerPosition()!
        const { x: stageX = 0, y: stageY = 0 } = this.stage.attrs
        pos.x = transform(pos.x, stageX, this.scale)
        pos.y = transform(pos.y, stageY, this.scale)
        let x = this.newRectangle.x
        let y = this.newRectangle.y
        let width = pos.x - x
        let height = pos.y - y
        if (width < 0) {
          x += width
          width = -width
        }
        if (height < 0) {
          y += height
          height = -height
        }
        const annotationToAdd = this.newRectangle.transform(x, y, width, height)
        this.newRectangle = null
        this.configStage.draggable = true
        this.$emit('add-rectangle', annotationToAdd.toProps())
      }
    },

    onMouseMove() {
      if (this.newRectangle) {
        const sx = this.newRectangle.x
        const sy = this.newRectangle.y
        const pos = this.stage.getPointerPosition()!
        const { x: stageX = 0, y: stageY = 0 } = this.stage.attrs
        pos.x = transform(pos.x, stageX, this.scale)
        pos.y = transform(pos.y, stageY, this.scale)
        this.newRectangle = this.newRectangle.transform(sx, sy, pos.x - sx, pos.y - sy)
      }
    },

    handleTransformEnd(e: Konva.KonvaEventObject<MouseEvent>) {
      // shape is transformed, let us save new attrs back to the node
      // find element in our state
      const rect = this.annotations.find((r) => r.id === this.selectedRectangle)
      // update the state
      if (rect) {
        const x = e.target.x()
        const y = e.target.y()
        const width = rect.width * e.target.scaleX()
        const height = rect.height * e.target.scaleY()
        const newRect = rect.transform(x, y, width, height)
        e.target.scaleX(1)
        e.target.scaleY(1)
        this.$emit('update-rectangle', newRect.toProps())
      }
    },

    onDragEnd(rect: Rectangle) {
      this.$emit('update-rectangle', rect.toProps())
    },

    removeRectangle(e: KeyboardEvent) {
      if (e.key === 'Backspace' || e.key === 'Delete') {
        if (this.selectedRectangle !== null) {
          this.$emit('delete-rectangle', this.selectedRectangle)
          this.selectedRectangle = null
          this.updateTransformer()
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
