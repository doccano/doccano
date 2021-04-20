<template>
  <base-card
    :disabled="!valid"
    :title="$t('labels.importTitle')"
    :agree-text="$t('generic.upload')"
    :cancel-text="$t('generic.cancel')"
    @agree="$emit('upload', file)"
    @cancel="cancel"
  >
    <template #content>
      <v-form
        ref="form"
        v-model="valid"
      >
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
          accept=".json"
          :error-messages="errorMessage"
          :label="$t('labels.filePlaceholder')"
          :rules="uploadSingleFileRules($t('rules.uploadFileRules'))"
          @change="$emit('clear')"
          @click:clear="$emit('clear')"
        />
      </v-form>
    </template>
  </base-card>
</template>

<script lang="ts">
import Vue from 'vue'
import BaseCard from '@/components/utils/BaseCard.vue'
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
  },

  methods: {
    cancel() {
      (this.$refs.form as HTMLFormElement).reset()
      this.$emit('cancel')
    }
  }
})
</script>
