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
            <v-bounding-box
              :rectangles="filteredRectangles"
              :highlight-id="highlightId"
              :image-url="imageUrl"
              :labels="bboxLabels"
              :selected-label="selectedLabel"
              :scale="scale"
              @add-rectangle="addRectangle"
              @update-rectangle="updateRectangle"
              @delete-rectangle="deleteRectangle"
              @update-scale="updateScale"
              @select-rectangle="selectRectangle"
            />
          </v-card>
        </v-col>
        <v-col cols="12" md="3">
          <list-metadata :metadata="meta" />
          <region-list
            class="mt-4"
            :regions="regionList"
            @change-visibility="changeVisibility"
            @delete-region="deleteRectangle"
            @hover-region="hoverRegion"
            @unhover-region="unhoverRegion"
          />
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
import VBoundingBox from '@/components/tasks/boundingBox/VBoundingBox.vue'
import ListMetadata from '@/components/tasks/metadata/ListMetadata'
import RegionList from '@/components/tasks/image/RegionList.vue'

export default {
  components: {
    ListMetadata,
    VBoundingBox,
    RegionList
  },

  layout: 'demo',

  data() {
    return {
      imageUrl: require('~/assets/images/demo/cat.jpeg'),
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
      selectedRectangle: undefined,
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
      return this.rectangles.map((rectangle) => {
        return {
          id: rectangle.id,
          category: this.labels.find((label) => rectangle.label === label.id).text,
          color: this.labels.find((label) => rectangle.label === label.id).backgroundColor,
          visibility: rectangle.id in this.visibilities ? this.visibilities[rectangle.id] : true
        }
      })
    },

    filteredRectangles() {
      return this.rectangles.filter((rectangle) => this.visibilities[rectangle.id] !== false)
    }
  },

  watch: {
    selectedLabel(newLabel) {
      if (newLabel !== undefined && !!this.selectedRectangle) {
        const rect = this.rectangles.find((r) => r.id === this.selectedRectangle.id)
        rect.label = newLabel.id
        this.updateRectangle(rect)
      }
    }
  },

  methods: {
    addRectangle(rectangle) {
      console.log('addRectangle', rectangle)
      this.rectangles.push(rectangle)
      this.visibilities[rectangle.id] = true
      this.selectedLabelIndex = undefined
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
      delete this.visibilities[rectangleId]
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

    selectRectangle(rectangleId) {
      console.log('selectRectangle', rectangleId)
      if (rectangleId) {
        this.selectedRectangle = this.rectangles.find((r) => r.id === rectangleId)
        this.selectedLabelIndex = this.labels.findIndex(
          (l) => l.id === this.selectedRectangle.label
        )
      } else {
        this.selectedRectangle = undefined
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
