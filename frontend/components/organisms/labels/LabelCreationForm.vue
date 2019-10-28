<template>
  <base-card
    title="Create Label"
    agree-text="Create"
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
      default: () => 'abcdefghijklmnopqrstuvwxyz'.split('')
    }
  },
  data() {
    return {
      valid: false,
      labelName: '',
      suffixKey: '',
      color: '',
      labelNameRules,
      colorRules
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
        this.createLabel({
          text: this.labelName,
          suffix_key: this.suffixKey,
          background_color: this.color
        })
        this.reset()
        this.cancel()
      }
    }
  }
}
</script>
