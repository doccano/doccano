<template>
  <v-card>
    <v-card-title>Create a Label Type</v-card-title>
    <v-card-text>
      <v-form ref="form" v-model="valid">
        <v-row>
          <v-col cols="12" sm="6">
            <v-text-field
              :value="text"
              :counter="100"
              :label="$t('labels.labelName')"
              :rules="[rules.required, rules.counter, rules.nameDuplicated]"
              outlined
              required
              @input="$emit('update:text', $event)"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-select
              :value="suffixKey"
              :items="availableSuffixKeys"
              :label="$t('labels.key')"
              :rules="[rules.keyDuplicated]"
              outlined
              @input="$emit('update:suffixKey', $event)"
            />
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" sm="12">
            <v-text-field
              :value="backgroundColor"
              :rules="[rules.validColor]"
              label="Color"
              hide-details="auto"
              outlined
              required
              @input="$emit('update:backgroundColor', $event)"
            />
            <v-chip-group v-model="selectedColorIndex" column mandatory>
              <v-chip
                v-for="color in predefinedColors"
                :key="color"
                :color="color"
                filter
                label
                style="height: 32px; width: 32px"
              />
              <v-tooltip bottom>
                <template #activator="{ on, attrs }">
                  <v-chip label v-bind="attrs" v-on="on" @click="setRandomColor">
                    <v-icon>{{ mdiReload }}</v-icon>
                  </v-chip>
                </template>
                <span>Random color</span>
              </v-tooltip>
            </v-chip-group>
          </v-col>
        </v-row>

        <v-row>
          <v-col>
            <div class="title black--text mb-2">Preview</div>
            <v-chip :color="backgroundColor" :text-color="textColor">
              {{ text }}
              <v-avatar v-if="suffixKey" right color="white" class="black--text font-weight-bold">
                {{ suffixKey }}
              </v-avatar>
            </v-chip>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" sm="12">
            <slot :valid="valid" />
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { mdiReload } from '@mdi/js'
import type { PropType } from 'vue'
import Vue from 'vue'
import { LabelDTO } from '~/services/application/label/labelData'

export default Vue.extend({
  props: {
    items: {
      type: Array as PropType<LabelDTO[]>,
      default: () => [],
      required: true
    },
    id: {
      type: Number as () => number | undefined,
      default: undefined
    },
    text: {
      type: String,
      required: true
    },
    backgroundColor: {
      type: String,
      required: true
    },
    suffixKey: {
      type: String as () => string | null,
      default: null
    }
  },

  data() {
    return {
      selectedColorIndex: 0,
      valid: false,
      rules: {
        required: (v: string) => !!v || 'Required',
        counter: (
          v: string // @ts-ignore
        ) => (v && v.length <= 100) || this.$t('rules.labelNameRules').labelLessThan100Chars,
        nameDuplicated: (
          v: string // @ts-ignore
        ) => !this.isUsedName(v) || this.$t('rules.labelNameRules').duplicated,
        keyDuplicated: (
          v: string // @ts-ignore
        ) => !this.isUsedSuffixKey(v) || this.$t('rules.keyNameRules').duplicated,
        validColor: (v: string) =>
          /^#[0-9A-F]{6}$/i.test(v) || 'This string is NOT a valid hex color.'
      },
      mdiReload
    }
  },

  computed: {
    availableSuffixKeys(): string[] {
      const usedSuffixKeys = this.items
        .map((item) => item.suffixKey)
        .filter((item) => item !== this.suffixKey)
      const allSuffixKeys = '0123456789abcdefghijklmnopqrstuvwxyz'.split('')
      return allSuffixKeys.filter((item) => !usedSuffixKeys.includes(item))
    },

    predefinedColors(): string[] {
      return [
        '#73D8FF',
        '#009CE0',
        '#0062B1',
        '#AEA1FF',
        '#7B64FF',
        '#653294',
        '#FDA1FF',
        '#FA28FF',
        '#AB149E',
        '#68CCCA',
        '#16A5A5',
        '#0C797D',
        '#A4DD00',
        '#68BC00',
        '#194D33',
        '#FCDC00',
        '#FCC400',
        '#FB9E00',
        '#F44E3B',
        '#D33115',
        '#9F0500'
      ]
    },

    textColor(): string {
      return this.$contrastColor(this.backgroundColor)
    }
  },

  watch: {
    selectedColorIndex(value) {
      if (value < this.predefinedColors.length) {
        this.$emit('update:backgroundColor', this.predefinedColors[this.selectedColorIndex])
      }
    }
  },

  methods: {
    isUsedName(text: string): boolean {
      return this.items.filter((item) => item.id !== this.id && item.text === text).length > 0
    },

    isUsedSuffixKey(key: string) {
      if (key === null) {
        return false
      }
      return this.items.filter((item) => item.id !== this.id && item.suffixKey === key).length > 0
    },

    setRandomColor() {
      const maxVal = 0xffffff
      const randomNumber = Math.floor(Math.random() * maxVal)
      const randomString = randomNumber.toString(16)
      const randColor = randomString.padStart(6, '0')
      this.$emit('update:backgroundColor', `#${randColor.toUpperCase()}`)
    }
  }
})
</script>
