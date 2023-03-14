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
        @click:clear-label="clear(image.id)"
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
      <v-snackbar
        :value="!!error"
        color="error"
        timeout="2000"
      >
        {{ error }}
      </v-snackbar>
      <v-card>
        <v-img contain :src="image.url" :max-height="imageSize.height" class="grey lighten-2" />
        <seq2seq-box
          :annotations="labels"
          @delete:annotation="(labelId) => remove(image.id, labelId)"
          @update:annotation="(labelId, text) => update(image.id, labelId, text)"
          @create:annotation="(text) => add(image.id, text)"
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
import { mdiFormatListBulleted, mdiText } from '@mdi/js'
import { toRefs, useContext } from '@nuxtjs/composition-api'
import _ from 'lodash'
import LayoutText from '@/components/tasks/layout/LayoutText'
import ListMetadata from '@/components/tasks/metadata/ListMetadata'
import AnnotationProgress from '@/components/tasks/sidebar/AnnotationProgress.vue'
import ToolbarLaptop from '@/components/tasks/toolbar/ToolbarLaptop'
import ToolbarMobile from '@/components/tasks/toolbar/ToolbarMobile'
import Seq2seqBox from '~/components/tasks/seq2seq/Seq2seqBox'
import { useTextLabel } from '~/composables/useTextLabel'

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
    const { app, params } = useContext()
    const { state, error, autoLabel, list, clear, remove, add, update } = useTextLabel(
      app.$repositories.textLabel,
      params.value.id
    )

    return {
      ...toRefs(state),
      error,
      add,
      autoLabel,
      list,
      clear,
      remove,
      update
    }
  },

  data() {
    return {
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
      progress: {}
    }
  },

  async fetch() {
    this.images = await this.$services.example.fetchOne(
      this.projectId,
      this.$route.query.page,
      this.$route.query.q,
      this.$route.query.isChecked,
      this.$route.query.ordering
    )
    const image = this.images.items[0]
    this.setImageSize(image)
    if (this.enableAutoLabeling) {
      await this.autoLabel(image.id)
    } else {
      await this.list(image.id)
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
    async enableAutoLabeling(val) {
      if (val && !this.image.isConfirmed) {
        await this.autoLabel(this.image.id)
      }
    }
  },

  async created() {
    this.project = await this.$services.project.findById(this.projectId)
    this.progress = await this.$repositories.metrics.fetchMyProgress(this.projectId)
  },

  methods: {
    async updateProgress() {
      this.progress = await this.$repositories.metrics.fetchMyProgress(this.projectId)
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
      img.src = val.url
    }
  }
}
</script>

<style scoped>
.text-pre-wrap {
  white-space: pre-wrap !important;
}
</style>
