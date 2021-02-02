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
          <span v-for="(example, index) in selectedFormat.examples" :key="index">
            {{ example }}<br>
          </span>
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
import BaseCard from '@/components/molecules/BaseCard'
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
        return this.selectedFormat.accept
      } else {
        return '.txt,.csv,.json,.jsonl'
      }
    }
  },

  methods: {
    cancel() {
      this.$emit('close')
    },
    validate() {
      return this.$refs.form.validate()
    },
    reset() {
      this.$refs.form.reset()
    },
    create() {
      if (this.validate()) {
        this.errors = []
        const promises = []
        const id = this.$route.params.id
        const type = this.selectedFormat.type
        this.file.forEach((item) => {
          promises.push({
            projectId: id,
            format: type,
            file: item
          })
        })
        let p = Promise.resolve()
        promises.forEach((item) => {
          p = p.then(() => this.uploadDocument(item)).catch(() => {
            this.errors.push(item.file.name)
            this.showError = true
          })
        })
        p.finally(() => {
          if (!this.errors.length) {
            this.reset()
            this.cancel()
          } else {
            this.errorMsg = this.errors.join(', ')
          }
        })
      }
    }
  }
}
</script>
