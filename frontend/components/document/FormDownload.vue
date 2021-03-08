<template>
  <base-card
    :disabled="!valid"
    title="Export Data"
    agree-text="Export"
    cancel-text="Cancel"
    @agree="download"
    @cancel="cancel"
  >
    <template #content>
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
        <h2>{{ $t('dataset.exportDataMessage2') }}</h2>
        <v-text-field
          v-model="filename"
          placeholder="Name the file"
          :rules="[v => !!v || 'File name is required']"
        />
        <v-checkbox
          v-model="onlyApproved"
          label="Export only approved documents"
          color="success"
          hide-details
        />
      </v-form>
    </template>
  </base-card>
</template>

<script lang="ts">
import Vue from 'vue'
import BaseCard from '@/components/molecules/BaseCard.vue'
import { fileFormatRules } from '@/rules/index'

export default Vue.extend({
  components: {
    BaseCard
  },

  props: {
    formats: {
      type: Array,
      default: () => [],
      required: true
    }
  },

  data() {
    return {
      file: null,
      filename: null,
      fileFormatRules,
      onlyApproved: false,
      selectedFormat: null,
      valid: false,
    }
  },

  methods: {
    cancel() {
      (this.$refs.format as HTMLFormElement).reset()
      this.$emit('cancel')
    },
    download() {
      this.$emit('download', this.selectedFormat, this.filename, this.onlyApproved)
      this.cancel()
    }
  }  
})
</script>
