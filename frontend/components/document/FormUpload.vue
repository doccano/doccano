<template>
  <base-card
    :disabled="!valid"
    :title="$t('dataset.importDataTitle')"
    :agree-text="$t('generic.upload')"
    :cancel-text="$t('generic.cancel')"
    @agree="create"
    @cancel="cancel"
  >
    <template #content>
      <v-form
        ref="form"
        v-model="valid"
      >
        <v-alert
          v-show="showError"
          v-model="showError"
          type="error"
          dismissible
        >
          {{ $t('errors.fileCannotUpload') + errorMsg }}
        </v-alert>
        <h2>{{ $t('dataset.importDataMessage1') }}</h2>
        <v-radio-group
          v-model="selectedFormat"
          :rules="fileFormatRules($t('rules.fileFormatRules'))"
        >
          <v-radio
            v-for="(format, i) in formats"
            :key="i"
            :label="format.text"
            :value="format"
          />
        </v-radio-group>
        <v-sheet
          v-if="selectedFormat"
          :dark="!$vuetify.theme.dark"
          :light="$vuetify.theme.dark"
          class="mb-5 pa-5"
        >
        <pre>{{ selectedFormat.example }}</pre>
        </v-sheet>
        <h2>{{ $t('dataset.importDataMessage2') }}</h2>
        <v-file-input
          v-model="file"
          multiple
          :accept="acceptType"
          :rules="uploadFileRules($t('rules.uploadFileRules'))"
          :label="$t('labels.filePlaceholder')"
        />
      </v-form>
    </template>
  </base-card>
</template>

<script>
import BaseCard from '@/components/utils/BaseCard'
import { fileFormatRules, uploadFileRules } from '@/rules/index'

export default {
  components: {
    BaseCard
  },
  props: {
    uploadDocument: {
      type: Function,
      default: () => {},
      required: true
    },
    formats: {
      type: Array,
      default: () => [],
      required: true
    }
  },
  data() {
    return {
      valid: false,
      file: null,
      selectedFormat: null,
      fileFormatRules,
      uploadFileRules,
      showError: false,
      errors: [],
      errorMsg: ''
    }
  },

  computed: {
    acceptType() {
      if (this.selectedFormat) {
        return `.${this.selectedFormat.extension}`
      } else {
        return '.txt'
      }
    }
  },

  methods: {
    cancel() {
      this.$emit('cancel')
    },
    reset() {
      this.$refs.form.reset()
    },
    create() {
      this.errors = []
      const promises = []
      const type = this.selectedFormat.type
      this.file.forEach((item) => {
        promises.push({
          format: type,
          file: item
        })
      })
      let p = Promise.resolve()
      promises.forEach((item) => {
        p = p.then(() => this.uploadDocument(item.file, item.format)).catch(() => {
          this.errors.push(item.file.name)
          this.showError = true
        })
      })
      p.finally(() => {
        if (!this.errors.length) {
          this.reset()
          this.$emit('success')
        } else {
          this.errorMsg = this.errors.join(', ')
        }
      })
    }
  }
}
</script>
