<template>
  <v-main>
    <v-container fluid>
      <v-row justify="center">
        <v-col cols="12" md="9">
          <v-card>
            <v-card-title>
              <v-chip-group v-model="selectedLabelIndex" column>
                <v-chip
                  v-for="item in labels"
                  :key="item.id"
                  :color="item.backgroundColor"
                  filter
                  :text-color="$contrastColor(item.backgroundColor)"
                >
                  {{ item.text }}
                  <v-avatar
                    v-if="item.suffixKey"
                    right
                    color="white"
                    class="black--text font-weight-bold"
                  >
                    {{ item.suffixKey }}
                  </v-avatar>
                </v-chip>
              </v-chip-group>
            </v-card-title>
            <v-divider />
            <v-segmentation
              :highlight-id="highlightId"
              :image-url="imageUrl"
              :labels="bboxLabels"
              :polygons="filteredRegions"
              :selected-label="selectedLabel"
              :scale="scale"
              @add-polygon="addPolygon"
              @delete-polygon="deletePolygon"
              @select-polygon="selectRegion"
              @update-polygon="updatePolygon"
              @update-scale="updateScale"
            />
          </v-card>
        </v-col>
        <v-col cols="12" md="3">
          <list-metadata :metadata="meta" />
          <region-list
            class="mt-4"
            :regions="regionList"
            @change-visibility="changeVisibility"
            @delete-region="deletePolygon"
            @hover-region="hoverRegion"
            @unhover-region="unhoverRegion"
          />
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
import VSegmentation from '@/components/tasks/segmentation/VSegmentation.vue'
import ListMetadata from '@/components/tasks/metadata/ListMetadata'
import RegionList from '@/components/tasks/image/RegionList.vue'

export default {
  components: {
    ListMetadata,
    VSegmentation,
    RegionList
  },

  layout: 'demo',

  data() {
    return {
      imageUrl: require('~/assets/images/demo/cat.jpeg'),
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
          id: 1,
          text: 'Cat',
          prefixKey: null,
          suffixKey: 'c',
          backgroundColor: '#7c20e0',
          textColor: '#ffffff'
        },
        {
          id: 2,
          text: 'Dog',
          prefixKey: null,
          suffixKey: 'd',
          backgroundColor: '#fbb028',
          textColor: '#000000'
        }
      ],
      meta: { wikiPageId: 2 },
      selectedLabelIndex: undefined,
      selectedPolygon: undefined,
      scale: 1,
      visibilities: {},
      highlightId: null
    }
  },

  computed: {
    bboxLabels() {
      return this.labels.map((label) => {
        return {
          id: label.id,
          name: label.text,
          color: label.backgroundColor
        }
      })
    },

    selectedLabel() {
      if (this.selectedLabelIndex !== undefined) {
        return this.labels[this.selectedLabelIndex]
      } else {
        return undefined
      }
    },

    regionList() {
      return this.polygons.map((polygon) => {
        return {
          id: polygon.id,
          category: this.labels.find((label) => polygon.label === label.id).text,
          color: this.labels.find((label) => polygon.label === label.id).backgroundColor,
          visibility: polygon.id in this.visibilities ? this.visibilities[polygon.id] : true
        }
      })
    },

    filteredRegions() {
      return this.polygons.filter((polygon) => this.visibilities[polygon.id] !== false)
    }
  },

  watch: {
    selectedLabel(newLabel) {
      if (newLabel !== undefined && !!this.selectedPolygon) {
        this.selectedPolygon.label = newLabel.id
        this.updatePolygon(this.selectedPolygon)
      }
    }
  },

  methods: {
    addPolygon(polygon) {
      this.polygons.push(polygon)
      this.selectedLabelIndex = undefined
    },

    deletePolygon(polygonId) {
      this.polygons = this.polygons.filter((p) => p.id !== polygonId)
    },

    updatePolygon(polygon) {
      console.log('updatePolygon', polygon)
      const index = this.polygons.findIndex((p) => p.id === polygon.id)
      if (index !== -1) {
        this.$set(this.polygons, index, polygon)
        this.selectedPolygon = polygon
      }
    },

    changeVisibility(regionId, visibility) {
      console.log('changeVisibility', regionId, visibility)
      this.$set(this.visibilities, regionId, visibility)
      this.visibilities = Object.assign({}, this.visibilities)
    },

    hoverRegion(regionId) {
      console.log('hoverRegion', regionId)
      this.highlightId = regionId
    },

    unhoverRegion(regionId) {
      console.log('unhoverRegion', regionId)
      this.highlightId = null
    },

    selectRegion(regionId) {
      console.log('selectRegion', regionId)
      if (regionId) {
        this.selectedPolygon = this.polygons.find((r) => r.id === regionId)
        this.selectedLabelIndex = this.labels.findIndex((l) => l.id === this.selectedPolygon.label)
      } else {
        this.selectedPolygon = undefined
        this.selectedLabelIndex = undefined
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
