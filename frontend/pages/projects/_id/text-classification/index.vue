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
      >
        <v-btn-toggle
          v-model="labelOption"
          mandatory
          class="ms-2"
        >
          <v-btn icon>
            <v-icon>mdi-format-list-bulleted</v-icon>
          </v-btn>
          <v-btn icon>
            <v-icon>mdi-text</v-icon>
          </v-btn>
        </v-btn-toggle>
      </toolbar-laptop>
      <toolbar-mobile
        :total="docs.count"
        class="d-flex d-sm-none"
      />
    </template>
    <template v-slot:content>
      <v-card
        v-shortkey="shortKeys"
        @shortkey="addOrRemove"
      >
        <v-card-title>
          <label-group
            v-if="labelOption === 0"
            :labels="labels"
            :annotations="annotations"
            :single-label="project.singleClassClassification"
            @add="add"
            @remove="remove"
          />
          <label-select
            v-else
            :labels="labels"
            :annotations="annotations"
            :single-label="project.singleClassClassification"
            @add="add"
            @remove="remove"
          />
        </v-card-title>
        <v-divider />
        <v-card-text class="title highlight" v-text="doc.text" />
      </v-card>
    </template>
    <template v-slot:sidebar>
      <list-metadata :metadata="doc.meta" />
    </template>
  </layout-text>
</template>

<script>
import _ from 'lodash'
import LabelGroup from '@/components/tasks/textClassification/LabelGroup'
import LabelSelect from '@/components/tasks/textClassification/LabelSelect'
import LayoutText from '@/components/tasks/layout/LayoutText'
import ListMetadata from '@/components/tasks/metadata/ListMetadata'
import ToolbarLaptop from '@/components/tasks/toolbar/ToolbarLaptop'
import ToolbarMobile from '@/components/tasks/toolbar/ToolbarMobile'

export default {
  layout: 'workspace',

  components: {
    LabelGroup,
    LabelSelect,
    LayoutText,
    ListMetadata,
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
      enableAutoLabeling: false,
      labelOption: 0
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
      const annotation = this.annotations.find(item => item.label === label.id)
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
