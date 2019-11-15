<template>
  <base-card
    title="Upload Data"
    agree-text="Upload"
    cancel-text="Cancel"
    :disabled="!valid"
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
          The file could not be uploaded. Maybe invalid format.
          Please check available formats carefully.
        </v-alert>
        <h2>Select a file format</h2>
        <v-radio-group
          v-model="selectedFormat"
          :rules="fileFormatRules"
        >
          <v-radio
            v-for="(format, i) in formats"
            :key="i"
            :label="format.text"
            :value="format"
          />
        </v-radio-group>
        <code
          v-if="selectedFormat"
          class="mb-10 pa-5 highlight"
        >
          <span v-for="(example, index) in selectedFormat.examples" :key="index">{{ example }}</span>
        </code>
        <h2>Select a file</h2>
        <v-file-input
          v-model="file"
          :accept="acceptType"
          :rules="uploadFileRules"
          label="File input"
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
      showError: false
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
        this.uploadDocument({
          projectId: this.$route.params.id,
          format: this.selectedFormat.type,
          file: this.file
        })
          .then((response) => {
            this.reset()
            this.cancel()
          })
          .catch(() => {
            this.showError = true
          })
      }
    }
  }
}
</script>

<style scoped>
  .highlight {
    font-size: 100%;
    width: 100%;
  }
  .highlight:before {
    content: ''
  }
</style>
