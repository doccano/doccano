<template>
  <base-card
    :disabled="!valid"
    :title="$t('labels.importTitle')"
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

<script>
import BaseCard from '@/components/molecules/BaseCard'
import { uploadSingleFileRules } from '@/rules/index'

export default {
  components: {
    BaseCard
  },
  props: {
    uploadLabel: {
      type: Function,
      default: () => {},
      required: true
    }
  },
  data() {
    return {
      valid: false,
      file: null,
      uploadSingleFileRules,
      showError: false
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
        this.uploadLabel({
          projectId: this.$route.params.id,
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
