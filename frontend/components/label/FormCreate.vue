<template>
  <base-card
    :disabled="!valid"
    :title="$t('labels.createLabel')"
    :agree-text="$t('generic.create')"
    :cancel-text="$t('generic.cancel')"
    @agree="$emit('save')"
    @cancel="$emit('cancel')"
  >
    <template #content>
      <v-form
        ref="form"
        v-model="valid"
      >
        <v-text-field
          v-model="item.text"
          :label="$t('labels.labelName')"
          :rules="labelNameRules($t('rules.labelNameRules'))"
          prepend-icon="label"
          single-line
          counter
          autofocus
        />
        <v-select
          v-model="item.suffix_key"
          :items="shortkeys"
          :label="$t('labels.key')"
          prepend-icon="mdi-keyboard"
        />
        <v-color-picker
          v-model="item.background_color"
          :rules="colorRules($t('rules.colorRules'))"
          show-swatches
          hide-mode-switch
          width="800"
        />
      </v-form>
    </template>
  </base-card>
</template>

<script lang="ts">
import Vue from 'vue'
import BaseCard from '@/components/molecules/BaseCard.vue'
import { colorRules, labelNameRules } from '@/rules/index'

export default Vue.extend({
  components: {
    BaseCard
  },

  props: {
    value: {
      type: Object,
      default: () => {},
      required: true
    }
  },

  data() {
    return {
      valid: false,
      labelNameRules,
      colorRules
    }
  },

  computed: {
    shortkeys() {
      return '0123456789abcdefghijklmnopqrstuvwxyz'.split('')
    },
    item: {
      get() {
        // Property '$emit' does not exist on type '() => any'
        // @ts-ignore
        return this.value
      },
      set(val) {
        // Property '$emit' does not exist on type '() => any'
        // @ts-ignore
        this.$emit('input', val)
      }
    }
  },

  methods: {
    hoge() {
      this.$emit('inpupt')
    }
  }
})
</script>
