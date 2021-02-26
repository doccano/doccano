<template>
  <base-card
    :disabled="!valid"
    :title="$t('labels.importTitle')"
    :agree-text="$t('generic.upload')"
    :cancel-text="$t('generic.cancel')"
    @agree="$emit('upload', file)"
    @cancel="$emit('cancel')"
  >
    <template #content>
      <v-form v-model="valid">
        <v-alert
          v-show="errorMessage"
          type="error"
          dismissible
        >
          {{ $t('errors.fileCannotUpload') }}
        </v-alert>
        <h2>{{ $t('labels.importMessage1') }}</h2>
        <v-sheet
          v-if="exampleFormat"
          :dark="!$vuetify.theme.dark"
          :light="$vuetify.theme.dark"
          class="mb-5 pa-5"
        >
          <pre>{{ exampleFormat }}</pre>
        </v-sheet>
        <h2>{{ $t('labels.importMessage2') }}</h2>
        <v-file-input
          v-model="file"
          :rules="uploadSingleFileRules($t('rules.uploadFileRules'))"
          accept=".json"
          :label="$t('labels.filePlaceholder')"
        />
      </v-form>
    </template>
  </base-card>
</template>

<script lang="ts">
import Vue from 'vue'
import BaseCard from '@/components/molecules/BaseCard.vue'
import { uploadSingleFileRules } from '@/rules/index'

export default Vue.extend({
  components: {
    BaseCard
  },

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
      uploadSingleFileRules,
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
