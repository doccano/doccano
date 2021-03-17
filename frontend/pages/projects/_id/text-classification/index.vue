<template>
  <layout-text v-if="doc.id">
    <template v-slot:header>
      <toolbar-laptop
        :doc-id="doc.id"
        :enable-auto-labeling.sync="enableAutoLabeling"
        :guideline-text="project.guideline"
        :is-reviewd="doc.isApproved"
        :show-approve-button="project.permitApprove"
        :total="docs.count"
        class="d-none d-sm-block"
        @click:clear-label="clear"
        @click:review="approve"
      />
      <toolbar-mobile
        :total="docs.count"
        class="d-flex d-sm-none"
      />
    </template>
    <template v-slot:content>
      <v-card @shortkey="addOrRemove">
        <v-card-title>
          <text-classification
            :labels="labels"
            :annotations="annotations"
            @add="add"
            @remove="remove"
          />
        </v-card-title>
        <v-card-text class="title highlight" v-text="doc.text" />
      </v-card>
    </template>
    <template v-slot:sidebar>
      <list-metadata :metadata="JSON.parse(doc.meta)" />
    </template>
  </layout-text>
</template>

<script>
import Vue from 'vue'
import _ from 'lodash'
import LayoutText from '@/components/tasks/layout/LayoutText'
import ListMetadata from '@/components/tasks/metadata/ListMetadata'
import TextClassification from '@/components/tasks/textClassification/TextClassification'
import ToolbarLaptop from '@/components/tasks/toolbar/ToolbarLaptop'
import ToolbarMobile from '@/components/tasks/toolbar/ToolbarMobile'
Vue.use(require('vue-shortkey'))

export default {
  layout: 'workspace',

  components: {
    LayoutText,
    ListMetadata,
    TextClassification,
    ToolbarLaptop,
    ToolbarMobile
  },

  async fetch() {
    this.docs = await this.$services.document.fetchOne(
      this.projectId,
      this.$route.query.page,
      this.$route.query.q,
      this.$route.query.isChecked,
      this.project.filterOption
    )
    const doc = this.docs.items[0]
    if (this.enableAutoLabeling) {
      await this.autoLabel(doc.id)
    }
    await this.list(doc.id)
  },

  data() {
    return {
      annotations: [],
      docs: [],
      labels: [],
      project: {},
      enableAutoLabeling: false
    }
  },

  computed: {
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
    this.project = await this.$services.project.findById(this.projectId)
  },

  methods: {
    async list(docId) {
      this.annotations = await this.$services.textClassification.list(this.projectId, docId)
    },

    async remove(id) {
      await this.$services.textClassification.delete(this.projectId, this.doc.id, id)
      await this.list(this.doc.id)
    },

    async add(labelId) {
      await this.$services.textClassification.create(this.projectId, this.doc.id, labelId)
      await this.list(this.doc.id)
    },

    async addOrRemove(event) {
      const label = this.labels.find(item => item.id === parseInt(event.srcKey, 10))
      const annotation = this.doc.annotations.find(item => item.label === label.id)
      if (annotation) {
        await this.remove(annotation.id)
      } else {
        await this.add(label.id)
      }
    },

    async clear() {
      await this.$services.textClassification.clear(this.projectId, this.doc.id)
      await this.list(this.doc.id)
    },

    async autoLabel(docId) {
      try {
        await this.$services.textClassification.autoLabel(this.projectId, docId)
      } catch (e) {
        console.log(e.response.data.detail)
      }
    },

    async approve() {
      const approved = !this.doc.isApproved
      await this.$services.document.approve(this.projectId, this.doc.id, approved)
      await this.$fetch()
    }
  },

  validate({ params, query }) {
    return /^\d+$/.test(params.id) && /^\d+$/.test(query.page)
  }
}
</script>
