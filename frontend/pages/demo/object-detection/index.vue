<template>
  <v-main>
    <v-container fluid>
      <v-row justify="center">
        <v-col cols="12" md="9">
          <v-card>
            <v-bounding-box
              :rectangles="rectangles"
              :image-url="imageUrl"
              :labels="labels"
              :selected-label="selectedLabel"
              :scale="scale"
              @add-rectangle="addRectangle"
              @update-rectangle="updateRectangle"
              @delete-rectangle="deleteRectangle"
              @update-scale="updateScale"
            />
          </v-card>
        </v-col>
        <v-col cols="12" md="3">
          <list-metadata :metadata="meta" />
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
import { VBoundingBox } from 'vue-image-annotator'
import ListMetadata from '@/components/tasks/metadata/ListMetadata'

export default {
  components: {
    ListMetadata,
    VBoundingBox
  },

  layout: 'demo',

  data() {
    return {
      imageUrl: 'https://www.pakutaso.com/shared/img/thumb/shikun20220402_122123_TP_V.jpg',
      rectangles: [
        {
          id: 'uuid',
          label: 1,
          x: 10,
          y: 10,
          width: 100,
          height: 100
        }
      ],
      labels: [
        {
          id: 0,
          name: 'pig',
          color: '#ff0000'
        },
        {
          id: 1,
          name: 'cat',
          color: '#00ff00'
        },
        {
          id: 2,
          name: 'dog',
          color: '#0000ff'
        }
      ],
      meta: { wikiPageId: 2 },
      selectedLabel: undefined,
      selectedPolygon: undefined,
      scale: 1
    }
  },

  methods: {
    selectLabel(index) {
      this.selectedLabel = this.labels[index]
    },

    resetLabel() {
      this.selectedLabel = undefined
    },

    addRectangle(rectangle) {
      console.log('addRectangle', rectangle)
      this.rectangles.push(rectangle)
    },

    updateRectangle(rectangle) {
      console.log('updateRectangle', rectangle)
      const index = this.rectangles.findIndex((r) => r.id === rectangle.id)
      if (index !== -1) {
        this.$set(this.rectangles, index, rectangle)
      }
    },

    deleteRectangle(rectangleId) {
      console.log('deleteRectangle', rectangleId)
      this.rectangles = this.rectangles.filter((r) => r.id !== rectangleId)
    },

    zoomOut() {
      this.scale -= 0.1
    },

    zoomIn() {
      this.scale += 0.1
    },

    updateScale(scale) {
      this.scale = scale
    }
  }
}
</script>
