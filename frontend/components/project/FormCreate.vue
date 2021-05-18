<template>
  <base-card
    :disabled="!valid"
    :title="$t('overview.createProjectTitle')"
    :agree-text="$t('generic.save')"
    :cancel-text="$t('generic.cancel')"
    @agree="$emit('save')"
    @cancel="$emit('cancel')"
  >
    <template #content>
      <v-form v-model="valid">
        <v-text-field
          :value="name"
          :rules="projectNameRules($t('rules.projectNameRules'))"
          :label="$t('overview.projectName')"
          prepend-icon="mdi-account-multiple"
          required
          autofocus
          @input="updateValue('name', $event)"
        />
        <v-text-field
          :value="description"
          :rules="descriptionRules($t('rules.descriptionRules'))"
          :label="$t('generic.description')"
          prepend-icon="mdi-clipboard-text"
          required
          @input="updateValue('description', $event)"
        />
        <v-select
          :value="projectType"
          :items="projectTypes"
          :rules="projectTypeRules($t('rules.projectTypeRules'))"
          :label="$t('overview.projectType')"
          prepend-icon="mdi-keyboard"
          required
          @input="updateValue('projectType', $event)"
        >
          <template v-slot:item="props">
            {{ translateTypeName(props.item, $t('overview.projectTypes')) }}
          </template>
          <template v-slot:selection="props">
            {{ translateTypeName(props.item, $t('overview.projectTypes')) }}
          </template>
        </v-select>
        <v-checkbox
          v-if="hasSingleLabelOption"
          :value="singleClassClassification"
          label="Allow single label"
          @change="updateValue('singleClassClassification', $event === true)"
        />
        <v-checkbox
          :value="enableRandomOrder"
          :label="$t('overview.randomizeDocOrder')"
          @change="updateValue('enableRandomOrder', $event === true)"
        />
        <v-checkbox
          :value="enableShareAnnotation"
          :label="$t('overview.shareAnnotations')"
          @change="updateValue('enableShareAnnotation', $event === true)"
        />
      </v-form>
    </template>
  </base-card>
</template>

<script lang="ts">
import Vue from 'vue'
import BaseCard from '@/components/utils/BaseCard.vue'
import { projectNameRules, descriptionRules, projectTypeRules } from '@/rules/index'

export default Vue.extend({
  components: {
    BaseCard
  },

  props: {
    name: {
      type: String,
      default: '',
      required: true
    },
    description: {
      type: String,
      default: '',
      required: true
    },
    projectType: {
      type: String,
      default: '',
      required: true
    },
    enableRandomOrder: {
      type: Boolean,
      default: false,
      required: true
    },
    enableShareAnnotation: {
      type: Boolean,
      default: false,
      required: true
    },
    singleClassClassification: {
      type: Boolean,
      default: false,
      required: true
    }
  },

  data() {
    return {
      valid: false,
      projectNameRules,
      projectTypeRules,
      descriptionRules
    }
  },

  computed: {
    projectTypes() {
      return [
        'DocumentClassification',
        'SequenceLabeling',
        'Seq2seq',
        'ImageClassification',
        'Speech2text',
      ]
    },
    hasSingleLabelOption() {
      return [
        'DocumentClassification',
        'ImageClassification',
      ].includes(this.projectType)
    }
  },

  methods: {
    updateValue(key: string, value: string) {
      this.$emit(`update:${key}`, value);
    },
    translateTypeName(type: string, types: string[]): string {
      const index = this.projectTypes.indexOf(type)
      return types[index]
    }
  }
})
</script>
