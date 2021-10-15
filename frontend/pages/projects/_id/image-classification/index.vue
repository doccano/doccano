<template>
  <layout-text v-if="image.id">
    <template v-slot:header>
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
        :total="images.count"
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
        <v-img
          contain
          :src="image.url"
          :max-height="imageSize.height"
          class="grey lighten-2"
        />
      </v-card>
    </template>
    <template v-slot:sidebar>
      <list-metadata :metadata="image.meta" />
    </template>
  </layout-text>
</template>

<script>
import _ from 'lodash'
import { toRefs } from '@nuxtjs/composition-api'
import LabelGroup from '@/components/tasks/textClassification/LabelGroup'
import LabelSelect from '@/components/tasks/textClassification/LabelSelect'
import LayoutText from '@/components/tasks/layout/LayoutText'
import ListMetadata from '@/components/tasks/metadata/ListMetadata'
import ToolbarLaptop from '@/components/tasks/toolbar/ToolbarLaptop'
import ToolbarMobile from '@/components/tasks/toolbar/ToolbarMobile'
import { useLabelList } from '@/composables/useLabelList'

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

  setup() {
    const { state, getLabelList, shortKeys } = useLabelList()

    return {
      ...toRefs(state),
      getLabelList,
      shortKeys,
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
      }
    }
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
  },

  methods: {
    async list(imageId) {
      this.annotations = await this.$services.textClassification.list(this.projectId, imageId)
    },

    async remove(id) {
      await this.$services.textClassification.delete(this.projectId, this.image.id, id)
      await this.list(this.image.id)
    },

    async add(labelId) {
      await this.$services.textClassification.create(this.projectId, this.image.id, labelId)
      await this.list(this.image.id)
    },

    async addOrRemove(event) {
      const labelId = parseInt(event.srcKey, 10)
      const annotation = this.annotations.find(item => item.label === labelId)
      if (annotation) {
        await this.remove(annotation.id)
      } else {
        await this.add(labelId)
      }
    },

    async clear() {
      await this.$services.textClassification.clear(this.projectId, this.image.id)
      await this.list(this.image.id)
    },

    async autoLabel(imageId) {
      try {
        await this.$services.textClassification.autoLabel(this.projectId, imageId)
      } catch (e) {
        console.log(e.response.data.detail)
      }
    },

    async confirm() {
      await this.$services.example.confirm(this.projectId, this.image.id)
      await this.$fetch()
    },

    setImageSize(val) {
      const img = new Image()
      const self = this
      img.onload = function() {
        self.imageSize.height = this.height
        self.imageSize.width = this.width
      }
      img.src = val.url
    }
  },

  validate({ params, query }) {
    return /^\d+$/.test(params.id) && /^\d+$/.test(query.page)
  }
}
</script>

<style scoped>
.text-pre-wrap {
  white-space: pre-wrap !important;
}
</style>
