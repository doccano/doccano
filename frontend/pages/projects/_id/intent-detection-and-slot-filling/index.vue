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
      <v-card v-shortkey="shortKeys" @shortkey="addOrRemoveCategory">
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
import LayoutText from '@/components/tasks/layout/LayoutText'
import ListMetadata from '@/components/tasks/metadata/ListMetadata'
import EntityEditor from '@/components/tasks/sequenceLabeling/EntityEditor.vue'
import AnnotationProgress from '@/components/tasks/sidebar/AnnotationProgress.vue'
import LabelGroup from '@/components/tasks/textClassification/LabelGroup'
import ToolbarLaptop from '@/components/tasks/toolbar/ToolbarLaptop'
import ToolbarMobile from '@/components/tasks/toolbar/ToolbarMobile'
import { Category } from '~/domain/models/tasks/category'

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
      this.$route.query.isChecked,
      this.$route.query.ordering
    )
    const doc = this.docs.items[0]
    if (this.enableAutoLabeling && !doc.isConfirmed) {
      await this.autoLabel(doc.id)
    }
    await this.listSpan(doc.id)
    await this.listCategory(doc.id)
  },

  computed: {
    ...mapGetters('auth', ['isAuthenticated', 'getUsername', 'getUserId']),
    ...mapGetters('config', ['isRTL']),

    projectId() {
      return this.$route.params.id
    },

    shortKeys() {
      return Object.fromEntries(this.categoryTypes.map((item) => [item.id, [item.suffixKey]]))
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
    async enableAutoLabeling(val) {
      if (val && !this.doc.isConfirmed) {
        await this.autoLabel(this.doc.id)
        await this.listSpan(this.doc.id)
        await this.listCategory(this.doc.id)
      }
    }
  },

  async created() {
    this.spanTypes = await this.$services.spanType.list(this.projectId)
    this.categoryTypes = await this.$services.categoryType.list(this.projectId)
    this.project = await this.$services.project.findById(this.projectId)
    this.progress = await this.$repositories.metrics.fetchMyProgress(this.projectId)
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
      this.categories = await this.$repositories.category.list(this.projectId, id)
    },

    async removeCategory(id) {
      await this.$repositories.category.delete(this.projectId, this.doc.id, id)
      await this.listCategory(this.doc.id)
    },

    async addCategory(labelId) {
      const category = Category.create(labelId)
      await this.$repositories.category.create(this.projectId, this.doc.id, category)
      await this.listCategory(this.doc.id)
    },

    async addOrRemoveCategory(event) {
      const labelId = parseInt(event.srcKey, 10)
      const category = this.categories.find((item) => item.label === labelId)
      if (category) {
        await this.removeCategory(category.id)
      } else {
        await this.addCategory(labelId)
      }
    },

    async clear() {
      await this.$repositories.category.clear(this.projectId, this.doc.id)
      await this.$services.sequenceLabeling.clear(this.projectId, this.doc.id)
      await this.listSpan(this.doc.id)
      await this.listCategory(this.doc.id)
    },

    async autoLabel(docId) {
      try {
        await this.$services.sequenceLabeling.autoLabel(this.projectId, docId)
      } catch (e) {
        console.log(e.response.data.detail)
      }
    },

    async updateProgress() {
      this.progress = await this.$repositories.metrics.fetchMyProgress(this.projectId)
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
