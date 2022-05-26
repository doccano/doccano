<template>
  <v-card>
    <v-card-title v-text="$t('labels.importLabels')" />
    <v-card-text>
      <v-form ref="form" v-model="valid">
        <h3>{{ $t('labels.importMessage1') }}</h3>
        <v-sheet
          v-if="exampleFormat"
          :dark="!$vuetify.theme.dark"
          :light="$vuetify.theme.dark"
          class="mb-5 pa-5"
        >
          <pre>{{ exampleFormat }}</pre>
        </v-sheet>
        <v-file-input
          v-model="file"
          accept=".json"
          :error-messages="errorMessage"
          :label="$t('labels.filePlaceholder')"
          :rules="uploadSingleFileRules($t('rules.uploadFileRules'))"
          outlined
          prepend-icon=""
          @change="$emit('clear')"
          @click:clear="$emit('clear')"
        />
        <v-btn
          :disabled="!valid"
          color="primary"
          class="text-capitalize"
          @click="$emit('upload', file)"
        >
          Import
        </v-btn>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import { uploadSingleFileRules } from '@/rules/index'

export default Vue.extend({
  props: {
    errorMessage: {
      type: String,
      default: ''
    }
  },

  data() {
    return {
      file: null,
      valid: false,
      uploadSingleFileRules
    }
  },

  computed: {
    exampleFormat() {
      const data = [
        {
          text: 'Dog',
          suffix_key: 'a',
          background_color: '#FF0000',
          text_color: '#ffffff'
        },
        {
          text: 'Cat',
          suffix_key: 'c',
          background_color: '#FF0000',
          text_color: '#ffffff'
        }
      ]
      return JSON.stringify(data, null, 4)
    }
  }
})
</script>
