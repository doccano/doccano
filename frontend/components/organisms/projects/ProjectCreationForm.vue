<template>
  <base-card
    :disabled="!valid"
    :title="$t('overview.createProjectTitle')"
    :agree-text="$t('generic.create')"
    :cancel-text="$t('generic.cancel')"
    @agree="create"
    @cancel="cancel"
  >
    <template #content>
      <v-form
        ref="form"
        v-model="valid"
      >
        <v-text-field
          v-model="name"
          :rules="projectNameRules($t('rules.projectNameRules'))"
          :label="$t('overview.projectName')"
          prepend-icon="mdi-account-multiple"
          data-test="project-name"
          required
          autofocus
        />
        <v-text-field
          v-model="description"
          :rules="descriptionRules($t('rules.descriptionRules'))"
          :label="$t('generic.description')"
          prepend-icon="mdi-clipboard-text"
          data-test="project-description"
          required
        />
        <v-select
          v-model="projectType"
          :items="$t('overview.projectTypes')"
          :rules="projectTypeRules($t('rules.projectTypeRules'))"
          :label="$t('overview.projectType')"
          prepend-icon="mdi-keyboard"
          data-test="project-type"
          required
        />
        <v-checkbox
          v-model="enableRandomizeDocOrder"
          :label="$t('overview.randomizeDocOrder')"
        />
        <v-checkbox
          v-model="enableShareAnnotation"
          :label="$t('overview.shareAnnotations')"
        />
      </v-form>
    </template>
  </base-card>
</template>

<script>
import BaseCard from '@/components/molecules/BaseCard'
import { projectNameRules, descriptionRules, projectTypeRules } from '@/rules/index'

export default {
  components: {
    BaseCard
  },
  props: {
    createProject: {
      type: Function,
      default: () => {},
      required: true
    }
  },
  data() {
    return {
      valid: false,
      name: '',
      description: '',
      projectType: null,
      enableShareAnnotation: false,
      enableRandomizeDocOrder: false,
      projectNameRules,
      projectTypeRules,
      descriptionRules
    }
  },

  methods: {
    cancel() {
      this.$emit('close')
    },
    getServerType() {
      if (this.projectType === this.$t('overview.textClassification')) {
        return 'DocumentClassification'
      } else if (this.projectType === this.$t('overview.sequenceLabeling')) {
        return 'SequenceLabeling'
      } else if (this.projectType === this.$t('overview.sequenceToSequence')) {
        return 'Seq2seq'
      }
    },
    getResourceType() {
      if (this.projectType === this.$t('overview.textClassification')) {
        return 'TextClassificationProject'
      } else if (this.projectType === this.$t('overview.sequenceLabeling')) {
        return 'SequenceLabelingProject'
      } else if (this.projectType === this.$t('overview.sequenceToSequence')) {
        return 'Seq2seqProject'
      }
    },
    validate() {
      return this.$refs.form.validate()
    },
    reset() {
      this.$refs.form.reset()
    },
    create() {
      if (this.validate()) {
        this.createProject({
          name: this.name,
          description: this.description,
          project_type: this.getServerType(),
          guideline: this.$t('guideline.writeGuidelinePrompt'),
          resourcetype: this.getResourceType(),
          randomize_document_order: this.enableRandomizeDocOrder,
          collaborative_annotation: this.enableShareAnnotation
        })
        this.reset()
        this.cancel()
      }
    }
  }
}
</script>
