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
          :value="text"
          :label="$t('labels.labelName')"
          :rules="[rules.required, rules.counter, rules.nameDuplicated]"
          :prepend-icon="mdiLabel"
          single-line
          counter
          autofocus
          @input="updateValue('text', $event)"
        />
        <v-select
          :value="suffixKey"
          :items="shortkeys"
          :label="$t('labels.key')"
          :rules="[rules.keyDuplicated]"
          :prepend-icon="mdiKeyboard"
          @input="updateValue('suffixKey', $event)"
        />
        <v-color-picker
          :value="backgroundColor"
          :rules="[rules.required]"
          show-swatches
          hide-mode-switch
          width="800"
          @input="updateValue('backgroundColor', $event)"
        />
      </v-form>
    </template>
  </base-card>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiLabel, mdiKeyboard } from '@mdi/js'
import BaseCard from '@/components/utils/BaseCard.vue'

export default Vue.extend({
  components: {
    BaseCard
  },

  props: {
    text: {
      type: String,
      default: '',
      required: true
    },
    suffixKey: {
      type: String,
      default: null,
    },
    backgroundColor: {
      type: String,
      default: '#ffffff',
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
        counter: (v: string) => (v && v.length <= 100) || this.$t('rules.labelNameRules').labelLessThan100Chars,
        // @ts-ignore
        nameDuplicated: (v: string) => (!this.usedNames.includes(v)) || this.$t('rules.labelNameRules').duplicated,
        // @ts-ignore
        keyDuplicated: (v: string) => !this.usedKeys.includes(v) || this.$t('rules.keyNameRules').duplicated,
      },
      mdiLabel,
      mdiKeyboard
    }
  },

  computed: {
    shortkeys() {
      return '0123456789abcdefghijklmnopqrstuvwxyz'.split('')
    }
  },

  methods: {
    updateValue(key: string, value: string) {
      this.$emit(`update:${key}`, value);
    }
  }
})
</script>
