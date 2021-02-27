<template>
  <base-card
    :disabled="!valid"
    :title="$t('labels.createLabel')"
    :agree-text="$t('generic.save')"
    :cancel-text="$t('generic.cancel')"
    @agree="$emit('save')"
    @cancel="$emit('cancel')"
  >
    <template #content>
      <v-form v-model="valid">
        <v-text-field
          v-model="item.text"
          :label="$t('labels.labelName')"
          :rules="[rules.required, rules.counter, rules.nameDuplicated]"
          prepend-icon="label"
          single-line
          counter
          autofocus
        />
        <v-select
          v-model="item.suffix_key"
          :items="shortkeys"
          :label="$t('labels.key')"
          :rules="[rules.keyDuplicated]"
          prepend-icon="mdi-keyboard"
        />
        <v-color-picker
          v-model="item.background_color"
          :rules="[rules.required]"
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

export default Vue.extend({
  components: {
    BaseCard
  },

  props: {
    value: {
      type: Object,
      default: () => {},
      required: true
    },
    usedNames: {
      type: Array,
      default: () => [],
      required: true
    },
    usedKeys: {
      type: Array,
      default: () => [],
      required: true
    }
  },

  data() {
    return {
      valid: false,
      rules: {
        required: (v: string) => !!v || 'Required',
        // @ts-ignore
        counter: (v: string) => (v && v.length <= 30) || this.$t('rules.labelNameRules').labelLessThan30Chars,
        // @ts-ignore
        nameDuplicated: (v: string) => (!this.usedNames.includes(v)) || this.$t('rules.labelNameRules').duplicated,
        // @ts-ignore
        keyDuplicated: (v: string) => !this.usedKeys.includes(v) || this.$t('rules.keyNameRules').duplicated,
      }
    }
  },

  computed: {
    shortkeys() {
      return '0123456789abcdefghijklmnopqrstuvwxyz'.split('')
    },
    item: {
      get() {
        // @ts-ignore
        return this.value
      },
      set(val) {
        // @ts-ignore
        this.$emit('input', val)
      }
    }
  }
})
</script>
