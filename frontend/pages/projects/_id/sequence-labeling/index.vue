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
      <toolbar-mobile
        :total="docs.count"
        class="d-flex d-sm-none"
      />
    </template>
    <template #content>
      <v-card>
        <div class="annotation-text pa-4">
          <entity-editor
            :dark="$vuetify.theme.dark"
            :rtl="isRTL"
            :text="doc.text"
            :entities="annotations"
            :entity-labels="labels"
            :relations="links"
            :relation-labels="linkTypes"
            :allow-overlapping="project.allowOverlapping"
            :grapheme-mode="project.graphemeMode"
            @addEntity="addEntity"
            @click:entity="updateEntity"
            @contextmenu:entity="deleteEntity"
          />
        </div>
      </v-card>
    </template>
    <template #sidebar>
      <list-metadata :metadata="doc.meta" />
    </template>
  </layout-text>
</template>

<script>
import _ from 'lodash'
import { mapGetters } from 'vuex'
import LayoutText from '@/components/tasks/layout/LayoutText'
import ListMetadata from '@/components/tasks/metadata/ListMetadata'
import ToolbarLaptop from '@/components/tasks/toolbar/ToolbarLaptop'
import ToolbarMobile from '@/components/tasks/toolbar/ToolbarMobile'
import EntityEditor from '@/components/tasks/sequenceLabeling/EntityEditor.vue'

export default {

  components: {
    EntityEditor,
    LayoutText,
    ListMetadata,
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
      labels: [],
      links: [],
      linkTypes: [],
      project: {},
      enableAutoLabeling: false,
      rtl: false,
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
    ...mapGetters('auth', ['isAuthenticated', 'getUsername', 'getUserId']),
    ...mapGetters('config', ['isRTL']),

    shortKeys() {
      return Object.fromEntries(this.labels.map(item => [item.id, [item.suffixKey]]))
    },
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
    this.labels = await this.$services.label.list(this.projectId)
    this.linkTypes = await this.$services.linkTypes.list(this.projectId)
    this.project = await this.$services.project.findById(this.projectId)
  },

  methods: {
    async list(docId) {
      const annotations = await this.$services.sequenceLabeling.list(this.projectId, docId);
      const links = await this.$services.sequenceLabeling.listLinks(this.projectId);
      this.annotations = annotations;
      this.links = links;
    },

    async deleteEntity(id) {
      await this.$services.sequenceLabeling.delete(this.projectId, this.doc.id, id)
      await this.list(this.doc.id)
    },

    async addEntity(startOffset, endOffset, labelId) {
      await this.$services.sequenceLabeling.create(this.projectId, this.doc.id, labelId, startOffset, endOffset)
      await this.list(this.doc.id)
    },

    async updateEntity(annotationId, labelId) {
      await this.$services.sequenceLabeling.changeLabel(this.projectId, this.doc.id, annotationId, labelId)
      await this.list(this.doc.id)
    },

    async clear() {
      await this.$services.sequenceLabeling.clear(this.projectId, this.doc.id)
      await this.list(this.doc.id)
    },

    async autoLabel(docId) {
      try {
        await this.$services.sequenceLabeling.autoLabel(this.projectId, docId)
      } catch (e) {
        console.log(e.response.data.detail)
      }
    },

    async confirm() {
      await this.$services.example.confirm(this.projectId, this.doc.id)
      await this.$fetch()
    },
  }
}
</script>

<style scoped>
.annotation-text {
  font-size: 1.25rem !important;
  font-weight: 500;
  line-height: 2rem;
  font-family: "Roboto", sans-serif !important;
  opacity: 0.6;
}
</style>
