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
      <v-card>
        <v-card-title>
          <label-group
            :labels="categoryTypes"
            :annotations="categories"
            :single-label="exclusive"
            @add="addCategory"
            @remove="removeCategory"
          />
        </v-card-title>
        <v-divider />
        <div class="annotation-text pa-4">
          <entity-editor
            :dark="$vuetify.theme.dark"
            :rtl="isRTL"
            :text="doc.text"
            :entities="spans"
            :entity-labels="spanTypes"
            @addEntity="addSpan"
            @click:entity="updateSpan"
            @contextmenu:entity="deleteSpan"
          />
        </div>
      </v-card>
    </template>
    <template #sidebar>
      <annotation-progress :progress="progress" />
      <list-metadata :metadata="doc.meta" class="mt-4" />
    </template>
  </layout-text>
</template>
<script>
import { mapGetters } from 'vuex'
import EntityEditor from '@/components/tasks/sequenceLabeling/EntityEditor.vue'
import LayoutText from '@/components/tasks/layout/LayoutText'
import ListMetadata from '@/components/tasks/metadata/ListMetadata'
import ToolbarLaptop from '@/components/tasks/toolbar/ToolbarLaptop'
import ToolbarMobile from '@/components/tasks/toolbar/ToolbarMobile'
import LabelGroup from '@/components/tasks/textClassification/LabelGroup'
import AnnotationProgress from '@/components/tasks/sidebar/AnnotationProgress.vue'

export default {
  components: {
    AnnotationProgress,
    EntityEditor,
    LayoutText,
    ListMetadata,
    LabelGroup,
    ToolbarLaptop,
    ToolbarMobile
  },

  layout: 'workspace',

  validate({ params, query }) {
    return /^\d+$/.test(params.id) && /^\d+$/.test(query.page)
  },

  data() {
    return {
      docs: [],
      spans: [],
      categories: [],
      spanTypes: [],
      categoryTypes: [],
      project: {},
      exclusive: false,
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
    await this.listSpan(doc.id)
    await this.listCategory(doc.id)
  },

  computed: {
    ...mapGetters('auth', ['isAuthenticated', 'getUsername', 'getUserId']),
    ...mapGetters('config', ['isRTL']),

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
    '$route.query': '$fetch'
  },

  async created() {
    this.spanTypes = await this.$services.spanType.list(this.projectId)
    this.categoryTypes = await this.$services.categoryType.list(this.projectId)
    this.project = await this.$services.project.findById(this.projectId)
    this.progress = await this.$services.metrics.fetchMyProgress(this.projectId)
  },

  methods: {
    async listSpan(docId) {
      const spans = await this.$services.sequenceLabeling.list(this.projectId, docId)
      this.spans = spans
    },

    async deleteSpan(id) {
      await this.$services.sequenceLabeling.delete(this.projectId, this.doc.id, id)
      await this.listSpan(this.doc.id)
    },

    async addSpan(startOffset, endOffset, labelId) {
      await this.$services.sequenceLabeling.create(
        this.projectId,
        this.doc.id,
        labelId,
        startOffset,
        endOffset
      )
      await this.listSpan(this.doc.id)
    },

    async updateSpan(annotationId, labelId) {
      await this.$services.sequenceLabeling.changeLabel(
        this.projectId,
        this.doc.id,
        annotationId,
        labelId
      )
      await this.listSpan(this.doc.id)
    },

    async listCategory(id) {
      this.categories = await this.$services.textClassification.list(this.projectId, id)
    },

    async removeCategory(id) {
      await this.$services.textClassification.delete(this.projectId, this.doc.id, id)
      await this.listCategory(this.doc.id)
    },

    async addCategory(labelId) {
      await this.$services.textClassification.create(this.projectId, this.doc.id, labelId)
      await this.listCategory(this.doc.id)
    },

    async clear() {
      await this.$services.sequenceLabeling.clear(this.projectId, this.doc.id)
      await this.listSpan(this.doc.id)
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
.annotation-text {
  font-size: 1.25rem !important;
  font-weight: 500;
  line-height: 2rem;
  font-family: 'Roboto', sans-serif !important;
  opacity: 0.6;
}
</style>
