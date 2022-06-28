<template>
  <v-main>
    <v-container fluid>
      <v-row justify="center">
        <v-col cols="12" md="9">
          <v-card>
            <v-segmentation
              :image-url="imageUrl"
              :labels="labels"
              :polygons="polygons"
              :selected-label="selectedLabel"
              :scale="scale"
              @add-polygon="addPolygon"
              @delete-polygon="deletePolygon"
              @select-polygon="selectPolygon"
              @update-polygon="updatePolygon"
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
import { VSegmentation } from 'vue-image-annotator'
import ListMetadata from '@/components/tasks/metadata/ListMetadata'

export default {
  components: {
    ListMetadata,
    VSegmentation
  },

  layout: 'demo',

  data() {
    return {
      imageUrl: 'https://www.pakutaso.com/shared/img/thumb/shikun20220402_122123_TP_V.jpg',
      polygons: [
        {
          id: 'uuid',
          label: 1,
          points: [372, 249, 284, 366, 450, 371]
        }
      ],
      task: 'bounding box',
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

    addPolygon(polygon) {
      this.polygons.push(polygon)
    },

    deletePolygon(polygonId) {
      this.polygons = this.polygons.filter((p) => p.id !== polygonId)
    },

    selectPolygon(id) {
      console.log('selectPolygon', id)
      this.selectedPolygon = this.polygons.find((p) => p.id === id)
    },

    updatePolygon(polygon) {
      console.log('updatePolygon', polygon)
      const index = this.polygons.findIndex((p) => p.id === polygon.id)
      if (index !== -1) {
        this.$set(this.polygons, index, polygon)
        this.selectedPolygon = polygon
      }
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
