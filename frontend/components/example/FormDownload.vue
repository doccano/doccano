<template>
  <base-card
    :disabled="!valid"
    title="Export Data"
    agree-text="Export"
    cancel-text="Cancel"
    @agree="downloadRequest"
    @cancel="cancel"
  >
    <template #content>
      <v-overlay :value="isProcessing">
        <v-progress-circular
          indeterminate
          size="64"
        />
      </v-overlay>
      <v-form
        ref="form"
        v-model="valid"
      >
        <h2>{{ $t('dataset.importDataMessage1') }}</h2>
        <v-radio-group
          ref="format"
          v-model="selectedFormat"
          :rules="fileFormatRules($t('rules.fileFormatRules'))"
        >
          <v-radio
            v-for="(format, i) in formats"
            :key="i"
            :label="format.name"
            :value="format"
          />
        </v-radio-group>
        <v-sheet
          v-if="selectedFormat"
          :dark="!$vuetify.theme.dark"
          :light="$vuetify.theme.dark"
          class="mb-5 pa-5"
        >
          <pre>{{ selectedFormat.example.trim() }}</pre>
        </v-sheet>
        <h2>{{ $t('dataset.exportDataMessage2') }}</h2>
        <v-checkbox
          v-model="exportApproved"
          label="Export only approved documents"
          hide-details
        />
      </v-form>
    </template>
  </base-card>
</template>

<script lang="ts">
import Vue from 'vue'
import BaseCard from '@/components/utils/BaseCard.vue'
import { fileFormatRules } from '@/rules/index'
import { FormatDTO } from '~/services/application/download/formatData'

export default Vue.extend({
  components: {
    BaseCard
  },

  data() {
    return {
      file: null,
      fileFormatRules,
      exportApproved: false,
      selectedFormat: null as any,
      formats: [] as FormatDTO[],
      taskId: '',
      polling: null,
      valid: false,
      isProcessing: false,
    }
  },

  computed: {
    projectId() {
      return this.$route.params.id
    }
  },

  async created() {
    this.formats = await this.$services.downloadFormat.list(this.projectId)
  },

  beforeDestroy() {
    // @ts-ignore
	  clearInterval(this.polling)
  },

  methods: {
    cancel() {
      (this.$refs.format as HTMLFormElement).reset()
      this.taskId = ''
      this.exportApproved = false
      this.selectedFormat = null
      this.isProcessing = false
      this.$emit('cancel')
    },
    async downloadRequest() {
      this.isProcessing = true
      this.taskId = await this.$services.download.request(this.projectId, this.selectedFormat.name, this.exportApproved)
      this.pollData()
    },
    pollData() {
      // @ts-ignore
		  this.polling = setInterval(async() => {
        if (this.taskId) {
          const res = await this.$services.taskStatus.get(this.taskId)
          if (res.ready) {
            this.$services.download.download(this.projectId, this.taskId)
            this.cancel()
          }
        }
  		}, 1000)
	  },
  }  
})
</script>
