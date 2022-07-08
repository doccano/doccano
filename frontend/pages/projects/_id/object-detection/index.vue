<template>
  <layout-text v-if="image.id">
    <template #header>
      <toolbar-laptop
        :doc-id="image.id"
        :enable-auto-labeling.sync="enableAutoLabeling"
        :guideline-text="project.guideline"
        :is-reviewd="image.isConfirmed"
        :total="images.count"
        class="d-none d-sm-block"
        @click:clear-label="clear"
        @click:review="confirm"
      >
        <button-zoom class="ms-2" @zoom-in="zoomIn" @zoom-out="zoomOut" />
      </toolbar-laptop>
      <toolbar-mobile :total="images.count" class="d-flex d-sm-none" />
    </template>
    <template #content>
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
          :rectangles="filteredRegions"
          :highlight-id="highlightId"
          :image-url="image.fileUrl"
          :labels="bboxLabels"
          :selected-label="selectedLabel"
          :scale="scale"
          @add-rectangle="add"
          @update-rectangle="update"
          @delete-rectangle="remove"
          @update-scale="updateScale"
          @select-rectangle="selectRegion"
        />
      </v-card>
    </template>
    <template #sidebar>
      <annotation-progress :progress="progress" />
      <list-metadata :metadata="image.meta" class="mt-4" />
      <region-list
        v-if="annotations.length > 0"
        class="mt-4"
        :regions="regionList"
        @change-visibility="changeVisibility"
        @delete-region="remove"
        @hover-region="hoverRegion"
        @unhover-region="unhoverRegion"
      />
    </template>
  </layout-text>
</template>

<script>
import _ from 'lodash'
import { mdiText, mdiFormatListBulleted } from '@mdi/js'
import { toRefs, useContext } from '@nuxtjs/composition-api'
import LayoutText from '@/components/tasks/layout/LayoutText'
import ListMetadata from '@/components/tasks/metadata/ListMetadata'
import ToolbarLaptop from '@/components/tasks/toolbar/ToolbarLaptop'
import ToolbarMobile from '@/components/tasks/toolbar/ToolbarMobile'
import { useLabelList } from '@/composables/useLabelList'
import AnnotationProgress from '@/components/tasks/sidebar/AnnotationProgress.vue'
import VBoundingBox from '@/components/tasks/boundingBox/VBoundingBox.vue'
import RegionList from '@/components/tasks/image/RegionList.vue'
import ButtonZoom from '@/components/tasks/toolbar/buttons/ButtonZoom.vue'

export default {
  components: {
    AnnotationProgress,
    ButtonZoom,
    LayoutText,
    ListMetadata,
    RegionList,
    ToolbarLaptop,
    ToolbarMobile,
    VBoundingBox
  },
  layout: 'workspace',

  validate({ params, query }) {
    return /^\d+$/.test(params.id) && /^\d+$/.test(query.page)
  },

  setup() {
    const { app } = useContext()
    const { state, getLabelList, shortKeys } = useLabelList(app.$services.categoryType)

    return {
      ...toRefs(state),
      getLabelList,
      shortKeys
    }
  },

  data() {
    return {
      annotations: [],
      images: [],
      project: {},
      enableAutoLabeling: false,
      mdiText,
      mdiFormatListBulleted,
      progress: {},
      highlightId: null,
      selectedLabelIndex: undefined,
      selectedRegion: undefined,
      visibilities: {},
      scale: 1
    }
  },

  async fetch() {
    this.images = await this.$services.example.fetchOne(
      this.projectId,
      this.$route.query.page,
      this.$route.query.q,
      this.$route.query.isChecked
    )
    const image = this.images.items[0]
    if (this.enableAutoLabeling) {
      await this.autoLabel(image.id)
    }
    await this.list(image.id)
  },

  computed: {
    projectId() {
      return this.$route.params.id
    },

    image() {
      if (_.isEmpty(this.images) || this.images.items.length === 0) {
        return {}
      } else {
        return this.images.items[0]
      }
    },

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
      return this.annotations.map((annotation) => {
        return {
          id: annotation.uuid,
          category: this.labels.find((label) => annotation.label === label.id).text,
          color: this.labels.find((label) => annotation.label === label.id).backgroundColor,
          visibility:
            annotation.uuid in this.visibilities ? this.visibilities[annotation.uuid] : true
        }
      })
    },

    filteredRegions() {
      return this.annotations
        .filter((annotation) => this.visibilities[annotation.uuid] !== false)
        .map((a) => {
          return {
            ...a,
            id: a.uuid
          }
        })
    }
  },

  watch: {
    '$route.query': '$fetch',
    enableAutoLabeling(val) {
      if (val) {
        this.list(this.image.id)
      }
    },

    async selectedLabel(newLabel) {
      if (newLabel !== undefined && !!this.selectedRegion) {
        this.selectedRegion.label = newLabel.id
        await this.$services.bbox.update(
          this.projectId,
          this.image.id,
          this.selectedRegion.id,
          this.selectedRegion
        )
        await this.list(this.image.id)
      }
    }
  },

  async created() {
    this.getLabelList(this.projectId)
    this.project = await this.$services.project.findById(this.projectId)
    this.progress = await this.$services.metrics.fetchMyProgress(this.projectId)
  },

  methods: {
    async list(imageId) {
      this.annotations = await this.$services.bbox.list(this.projectId, imageId)
    },

    async remove(id) {
      delete this.visibilities[id]
      const bbox = this.annotations.find((a) => a.uuid === id)
      await this.$services.bbox.delete(this.projectId, this.image.id, bbox.id)
      await this.list(this.image.id)
    },

    async add(region) {
      this.visibilities[region.id] = true
      await this.$services.bbox.create(
        this.projectId,
        this.image.id,
        region.id,
        region.label,
        region.x,
        region.y,
        region.width,
        region.height
      )
      await this.list(this.image.id)
    },

    async update(region) {
      const bbox = this.annotations.find((a) => a.uuid === region.id)
      await this.$services.bbox.update(this.projectId, this.image.id, bbox.id, region)
      await this.list(this.image.id)
    },

    changeVisibility(regionId, visibility) {
      this.$set(this.visibilities, regionId, visibility)
      this.visibilities = Object.assign({}, this.visibilities)
    },

    async clear() {
      await this.$services.bbox.clear(this.projectId, this.image.id)
      await this.list(this.image.id)
    },

    async autoLabel(imageId) {
      try {
        await this.$services.bbox.autoLabel(this.projectId, imageId)
      } catch (e) {
        console.log(e.response.data.detail)
      }
    },

    async updateProgress() {
      this.progress = await this.$services.metrics.fetchMyProgress(this.projectId)
    },

    async confirm() {
      await this.$services.example.confirm(this.projectId, this.image.id)
      await this.$fetch()
      this.updateProgress()
    },

    hoverRegion(regionId) {
      this.highlightId = regionId
    },

    unhoverRegion() {
      this.highlightId = null
    },

    selectRegion(regionId) {
      if (regionId) {
        this.selectedRegion = this.annotations.find((r) => r.uuid === regionId)
        this.selectedLabelIndex = this.labels.findIndex((l) => l.id === this.selectedRegion.label)
      } else {
        this.selectedRegion = undefined
        this.selectedLabelIndex = undefined
      }
    },

    updateScale(scale) {
      this.scale = scale
    },

    zoomOut() {
      this.scale -= 0.1
    },

    zoomIn() {
      this.scale += 0.1
    }
  }
}
</script>

<style scoped>
.text-pre-wrap {
  white-space: pre-wrap !important;
}
</style>
