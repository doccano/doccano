<template>
  <v-card>
    <v-card-title>
      {{ $t('dataset.exportDataTitle') }}
    </v-card-title>
    <v-card-text>
      <v-overlay :value="isProcessing">
        <v-progress-circular indeterminate size="64" />
      </v-overlay>
      <v-form ref="form" v-model="valid">
        <v-select
          v-model="selectedFormat"
          :items="formats"
          hide-details="auto"
          item-text="name"
          label="File format"
          outlined
          :rules="fileFormatRules($t('rules.fileFormatRules'))"
        />
        <v-sheet
          v-if="selectedFormat"
          :dark="!$vuetify.theme.dark"
          :light="$vuetify.theme.dark"
          class="mt-2 pa-5"
        >
          <pre>{{ example }}</pre>
        </v-sheet>
        <v-checkbox v-model="exportApproved" label="Export only approved documents" hide-details />
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-btn class="text-capitalize ms-2 primary" :disabled="!valid" @click="downloadRequest">
        {{ $t('generic.export') }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import { fileFormatRules } from '@/rules/index'
import { Format } from '~/domain/models/download/format'

export default Vue.extend({
  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject', 'isProjectAdmin'],

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  data() {
    return {
      exportApproved: false,
      file: null,
      fileFormatRules,
      formats: [] as Format[],
      isProcessing: false,
      polling: null,
      selectedFormat: null as any,
      taskId: '',
      valid: false
    }
  },

  computed: {
    projectId() {
      return this.$route.params.id
    },

    example(): string {
      const item = this.formats.find((item: Format) => item.name === this.selectedFormat)
      return item!.example.trim()
    }
  },

  async created() {
    this.formats = await this.$repositories.downloadFormat.list(this.projectId)
  },

  beforeDestroy() {
    // @ts-ignore
    clearInterval(this.polling)
  },

  methods: {
    reset() {
      ;(this.$refs.form as HTMLFormElement).reset()
      this.taskId = ''
      this.exportApproved = false
      this.selectedFormat = null
      this.isProcessing = false
    },

    async downloadRequest() {
      this.isProcessing = true
      this.taskId = await this.$repositories.download.prepare(
        this.projectId,
        this.selectedFormat,
        this.exportApproved
      )
      this.pollData()
    },

    pollData() {
      // @ts-ignore
      this.polling = setInterval(async () => {
        if (this.taskId) {
          const res = await this.$repositories.taskStatus.get(this.taskId)
          if (res.ready) {
            this.$repositories.download.download(this.projectId, this.taskId)
            this.reset()
          }
        }
      }, 1000)
    }
  }
})
</script>
