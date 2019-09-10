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
    }
  },
  data() {
    return {
      valid: false,
      file: null,
      selectedFormat: null,
      formats: [
        {
          type: 'csv',
          text: 'Upload a CSV file from your computer',
          accept: '.csv'
        },
        {
          type: 'plain',
          text: 'Upload text items from your computer',
          accept: '.txt'
        },
        {
          type: 'json',
          text: 'Upload a JSON file from your computer',
          accept: '.json,.jsonl'
        }
      ],
      fileFormatRules,
      uploadFileRules
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
          format: this.selectedFormat,
          file: this.file
        })
        this.reset()
        this.cancel()
      }
    }
  }
}
</script>
