<template>
  <base-card
    title="Export Data"
    agree-text="Export"
    cancel-text="Cancel"
    :disabled="!valid"
    @agree="download"
    @cancel="cancel"
  >
    <template #content>
      <v-form
        ref="form"
        v-model="valid"
      >
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
    exportDocument: {
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
    download() {
      if (this.validate()) {
        this.exportDocument({
          projectId: this.$route.params.id,
          format: this.selectedFormat.type
        })
        this.reset()
        this.cancel()
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
