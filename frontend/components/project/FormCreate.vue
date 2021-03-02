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
          v-model="item.name"
          :rules="projectNameRules($t('rules.projectNameRules'))"
          :label="$t('overview.projectName')"
          prepend-icon="mdi-account-multiple"
          required
          autofocus
        />
        <v-text-field
          v-model="item.description"
          :rules="descriptionRules($t('rules.descriptionRules'))"
          :label="$t('generic.description')"
          prepend-icon="mdi-clipboard-text"
          required
        />
        <v-select
          v-model="item.projectType"
          :items="projectTypes"
          :rules="projectTypeRules($t('rules.projectTypeRules'))"
          :label="$t('overview.projectType')"
          prepend-icon="mdi-keyboard"
          required
        >
          <template v-slot:item="props">
            {{ translateTypeName(props.item, $t('overview.projectTypes')) }}
          </template>
          <template v-slot:selection="props">
            {{ translateTypeName(props.item, $t('overview.projectTypes')) }}
          </template>
          </v-select>
        <v-checkbox
          v-model="item.enableRandomizeDocOrder"
          :label="$t('overview.randomizeDocOrder')"
        />
        <v-checkbox
          v-model="item.enableShareAnnotation"
          :label="$t('overview.shareAnnotations')"
        />
      </v-form>
    </template>
  </base-card>
</template>

<script lang="ts">
import Vue from 'vue'
import BaseCard from '@/components/molecules/BaseCard.vue'
import { projectNameRules, descriptionRules, projectTypeRules } from '@/rules/index'

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
      projectNameRules,
      projectTypeRules,
      descriptionRules
    }
  },

  computed: {
    projectTypes() {
      return ['DocumentClassification', 'SequenceLabeling', 'Seq2seq']
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
  },

  methods: {
    translateTypeName(type: string, types: string[]): string {
      // @ts-ignore
      const index = this.projectTypes.indexOf(type)
      return types[index]
    }
  }
})
</script>
