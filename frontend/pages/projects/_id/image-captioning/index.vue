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
        <v-btn-toggle v-model="labelOption" mandatory class="ms-2">
          <v-btn icon>
            <v-icon>{{ mdiFormatListBulleted }}</v-icon>
          </v-btn>
          <v-btn icon>
            <v-icon>{{ mdiText }}</v-icon>
          </v-btn>
        </v-btn-toggle>
      </toolbar-laptop>
      <toolbar-mobile :total="images.count" class="d-flex d-sm-none" />
    </template>
    <template #content>
      <v-card>
        <v-img contain :src="image.fileUrl" :max-height="imageSize.height" class="grey lighten-2" />
        <seq2seq-box
          :annotations="annotations"
          @delete:annotation="remove"
          @update:annotation="update"
          @create:annotation="add"
        />
      </v-card>
    </template>
    <template #sidebar>
      <annotation-progress :progress="progress" />
      <list-metadata :metadata="image.meta" class="mt-4" />
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
import Seq2seqBox from '~/components/tasks/seq2seq/Seq2seqBox'

export default {
  components: {
    AnnotationProgress,
    LayoutText,
    ListMetadata,
    Seq2seqBox,
    ToolbarLaptop,
    ToolbarMobile
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
      labelOption: 0,
      imageSize: {
        height: 0,
        width: 0
      },
      mdiText,
      mdiFormatListBulleted,
      progress: {},
      headers: [
        {
          text: 'Text',
          align: 'left',
          value: 'text'
        },
        {
          text: 'Actions',
          align: 'right',
          value: 'action'
        }
      ]
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
    this.setImageSize(image)
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
    }
  },

  watch: {
    '$route.query': '$fetch',
    enableAutoLabeling(val) {
      if (val) {
        this.list(this.image.id)
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
      this.annotations = await this.$services.seq2seq.list(this.projectId, imageId)
    },

    async remove(id) {
      await this.$services.seq2seq.delete(this.projectId, this.image.id, id)
      await this.list(this.image.id)
    },

    async add(text) {
      await this.$services.seq2seq.create(this.projectId, this.image.id, text)
      await this.list(this.image.id)
    },

    async update(annotationId, text) {
      await this.$services.seq2seq.changeText(this.projectId, this.image.id, annotationId, text)
      await this.list(this.image.id)
    },

    async clear() {
      await this.$services.seq2seq.clear(this.projectId, this.image.id)
      await this.list(this.image.id)
    },

    async autoLabel(imageId) {
      try {
        await this.$services.seq2seq.autoLabel(this.projectId, imageId)
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

    setImageSize(val) {
      const img = new Image()
      const self = this
      img.onload = function () {
        self.imageSize.height = this.height
        self.imageSize.width = this.width
      }
      img.src = val.fileUrl
    }
  }
}
</script>

<style scoped>
.text-pre-wrap {
  white-space: pre-wrap !important;
}
</style>
