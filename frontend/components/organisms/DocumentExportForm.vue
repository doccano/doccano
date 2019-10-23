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
        <v-radio-group
          v-model="selectedFormat"
          :rules="fileFormatRules"
        >
          <v-radio
            v-for="(format, i) in formats"
            :key="i"
            :label="format"
            :value="format"
          />
        </v-radio-group>
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
          format: this.selectedFormat
        })
        this.reset()
        this.cancel()
      }
    }
  }
}
</script>
