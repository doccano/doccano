<template>
  <base-card
    :disabled="!valid"
    @agree="create"
    @cancel="reset"
    title="Create Label"
    agree-text="Create"
    cancel-text="Cancel"
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
          The label could not be created.
          You cannot use same label name or shortcut key.
        </v-alert>
        <v-text-field
          v-model="labelName"
          :rules="labelNameRules"
          label="Label name"
          prepend-icon="label"
        />
        <v-select
          v-model="suffixKey"
          :items="keys"
          label="Key"
          prepend-icon="mdi-keyboard"
        />
        <v-color-picker
          v-model="color"
          :rules="colorRules"
          show-swatches
          hide-mode-switch
          width="800"
          mode="hexa"
          class="ma-2"
        />
      </v-form>
    </template>
  </base-card>
</template>

<script>
import BaseCard from '@/components/molecules/BaseCard'
import { colorRules, labelNameRules } from '@/rules/index'

export default {
  components: {
    BaseCard
  },
  props: {
    createLabel: {
      type: Function,
      default: () => {},
      required: true
    },
    keys: {
      type: Array,
      default: () => [],
      required: true
    }
  },
  data() {
    return {
      valid: false,
      labelName: '',
      suffixKey: '',
      color: '',
      labelNameRules,
      colorRules,
      showError: false
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
      this.cancel('close')
    },
    create() {
      if (this.validate()) {
        this.createLabel({
          projectId: this.$route.params.id,
          text: this.labelName,
          prefix_key: null,
          suffix_key: this.suffixKey ? this.suffixKey : null,
          background_color: this.color.slice(0, 7), // #12345678 -> #123456
          text_color: '#ffffff'
        })
          .then(() => {
            this.reset()
          })
          .catch(() => {
            this.showError = true
          })
      }
    }
  }
}
</script>
