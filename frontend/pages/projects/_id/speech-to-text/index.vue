<template>
  <layout-text v-if="item.id">
    <template #header>
      <toolbar-laptop
        :doc-id="item.id"
        :enable-auto-labeling.sync="enableAutoLabeling"
        :guideline-text="project.guideline"
        :is-reviewd="item.isConfirmed"
        :total="items.count"
        class="d-none d-sm-block"
        @click:clear-label="clear"
        @click:review="confirm"
      />
      <toolbar-mobile :total="items.count" class="d-flex d-sm-none" />
    </template>
    <template #content>
      <v-overlay :value="isLoading">
        <v-progress-circular indeterminate size="64" />
      </v-overlay>
      <audio-viewer :source="item.fileUrl" class="mb-5" />
      <seq2seq-box
        :text="item.text"
        :annotations="annotations"
        @delete:annotation="remove"
        @update:annotation="update"
        @create:annotation="add"
      />
    </template>
    <template #sidebar>
      <annotation-progress :progress="progress" />
      <list-metadata :metadata="item.meta" class="mt-4" />
    </template>
  </layout-text>
</template>

<script>
import _ from 'lodash'
import LayoutText from '@/components/tasks/layout/LayoutText'
import ListMetadata from '@/components/tasks/metadata/ListMetadata'
import ToolbarLaptop from '@/components/tasks/toolbar/ToolbarLaptop'
import ToolbarMobile from '@/components/tasks/toolbar/ToolbarMobile'
import AnnotationProgress from '@/components/tasks/sidebar/AnnotationProgress.vue'
import Seq2seqBox from '~/components/tasks/seq2seq/Seq2seqBox'
import AudioViewer from '~/components/tasks/audio/AudioViewer'

export default {
  components: {
    AnnotationProgress,
    AudioViewer,
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

  data() {
    return {
      annotations: [],
      items: [],
      project: {},
      enableAutoLabeling: false,
      isLoading: false,
      progress: {}
    }
  },

  async fetch() {
    this.isLoading = true
    this.items = await this.$services.example.fetchOne(
      this.projectId,
      this.$route.query.page,
      this.$route.query.q,
      this.$route.query.isChecked
    )
    const item = this.items.items[0]
    if (this.enableAutoLabeling) {
      await this.autoLabel(item.id)
    }
    await this.list(item.id)
    this.isLoading = false
  },

  computed: {
    projectId() {
      return this.$route.params.id
    },
    item() {
      if (_.isEmpty(this.items) || this.items.items.length === 0) {
        return {}
      } else {
        return this.items.items[0]
      }
    }
  },

  watch: {
    '$route.query': '$fetch',
    enableAutoLabeling(val) {
      if (val) {
        this.list(this.item.id)
      }
    }
  },

  async created() {
    this.project = await this.$services.project.findById(this.projectId)
    this.progress = await this.$services.metrics.fetchMyProgress(this.projectId)
  },

  methods: {
    async list(itemId) {
      this.annotations = await this.$services.seq2seq.list(this.projectId, itemId)
    },

    async remove(id) {
      await this.$services.seq2seq.delete(this.projectId, this.item.id, id)
      await this.list(this.item.id)
    },

    async add(text) {
      await this.$services.seq2seq.create(this.projectId, this.item.id, text)
      await this.list(this.item.id)
    },

    async update(annotationId, text) {
      await this.$services.seq2seq.changeText(this.projectId, this.item.id, annotationId, text)
      await this.list(this.item.id)
    },

    async clear() {
      await this.$services.seq2seq.clear(this.projectId, this.item.id)
      await this.list(this.item.id)
    },

    async autoLabel(itemId) {
      try {
        await this.$services.seq2seq.autoLabel(this.projectId, itemId)
      } catch (e) {
        console.log(e.response.data.detail)
      }
    },

    async updateProgress() {
      this.progress = await this.$services.metrics.fetchMyProgress(this.projectId)
    },

    async confirm() {
      await this.$services.example.confirm(this.projectId, this.item.id)
      await this.$fetch()
      this.updateProgress()
    }
  }
}
</script>

<style scoped>
.text-pre-wrap {
  white-space: pre-wrap !important;
}
</style>
