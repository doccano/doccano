<template>
  <layout-text v-if="doc.id">
    <template #header>
      <toolbar-laptop
        :doc-id="doc.id"
        :enable-auto-labeling.sync="enableAutoLabeling"
        :guideline-text="project.guideline"
        :is-reviewd="doc.isConfirmed"
        :total="docs.count"
        class="d-none d-sm-block"
        @click:clear-label="clear"
        @click:review="confirm"
      />
      <toolbar-mobile :total="docs.count" class="d-flex d-sm-none" />
    </template>
    <template #content>
      <v-card class="mb-5">
        <v-card-text class="title text-pre-wrap" v-text="doc.text" />
      </v-card>
      <seq2seq-box
        :text="doc.text"
        :annotations="annotations"
        @delete:annotation="remove"
        @update:annotation="update"
        @create:annotation="add"
      />
    </template>
    <template #sidebar>
      <annotation-progress :progress="progress" />
      <list-metadata :metadata="doc.meta" class="mt-4" />
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

  data() {
    return {
      annotations: [],
      docs: [],
      project: {},
      enableAutoLabeling: false,
      progress: {}
    }
  },

  async fetch() {
    this.docs = await this.$services.example.fetchOne(
      this.projectId,
      this.$route.query.page,
      this.$route.query.q,
      this.$route.query.isChecked
    )
    const doc = this.docs.items[0]
    if (this.enableAutoLabeling) {
      await this.autoLabel(doc.id)
    }
    await this.list(doc.id)
  },

  computed: {
    projectId() {
      return this.$route.params.id
    },
    doc() {
      if (_.isEmpty(this.docs) || this.docs.items.length === 0) {
        return {}
      } else {
        return this.docs.items[0]
      }
    }
  },

  watch: {
    '$route.query': '$fetch',
    enableAutoLabeling(val) {
      if (val) {
        this.list(this.doc.id)
      }
    }
  },

  async created() {
    this.project = await this.$services.project.findById(this.projectId)
    this.progress = await this.$services.metrics.fetchMyProgress(this.projectId)
  },

  methods: {
    async list(docId) {
      this.annotations = await this.$services.seq2seq.list(this.projectId, docId)
    },

    async remove(id) {
      await this.$services.seq2seq.delete(this.projectId, this.doc.id, id)
      await this.list(this.doc.id)
    },

    async add(text) {
      await this.$services.seq2seq.create(this.projectId, this.doc.id, text)
      await this.list(this.doc.id)
    },

    async update(annotationId, text) {
      await this.$services.seq2seq.changeText(this.projectId, this.doc.id, annotationId, text)
      await this.list(this.doc.id)
    },

    async clear() {
      await this.$services.seq2seq.clear(this.projectId, this.doc.id)
      await this.list(this.doc.id)
    },

    async autoLabel(docId) {
      try {
        await this.$services.seq2seq.autoLabel(this.projectId, docId)
      } catch (e) {
        console.log(e.response.data.detail)
      }
    },

    async updateProgress() {
      this.progress = await this.$services.metrics.fetchMyProgress(this.projectId)
    },

    async confirm() {
      await this.$services.example.confirm(this.projectId, this.doc.id)
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
