<template>
  <base-card
    title="Add Project"
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
          v-model="name"
          :rules="projectNameRules"
          label="Project name"
          prepend-icon="mdi-account-multiple"
          data-test="project-name"
          required
          autofocus
        />
        <v-text-field
          v-model="description"
          :rules="descriptionRules"
          label="Description"
          prepend-icon="mdi-clipboard-text"
          data-test="project-description"
          required
        />
        <v-select
          v-model="projectType"
          :items="projectTypes"
          :rules="projectTypeRules"
          label="projectType"
          prepend-icon="mdi-keyboard"
          data-test="project-type"
          required
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
    },
    projectTypes: {
      type: Array,
      default: () => [
        'Text Classification',
        'Sequence Labeling',
        'Sequence to sequence'
      ] // Todo: Get project types from backend server.
    }
  },
  data() {
    return {
      valid: false,
      name: '',
      description: '',
      projectType: null,
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
      if (this.projectType === 'Text Classification') {
        return 'DocumentClassification'
      } else if (this.projectType === 'Sequence Labeling') {
        return 'SequenceLabeling'
      } else if (this.projectType === 'Sequence to sequence') {
        return 'Seq2seq'
      }
    },
    getResourceType() {
      if (this.projectType === 'Text Classification') {
        return 'TextClassificationProject'
      } else if (this.projectType === 'Sequence Labeling') {
        return 'SequenceLabelingProject'
      } else if (this.projectType === 'Sequence to sequence') {
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
          guideline: 'Please write annotation guideline.',
          resourcetype: this.getResourceType()
          // randomize_document_order: this.randomizeDocumentOrder,
          // collaborative_annotation: this.collaborativeAnnotation
        })
        this.reset()
        this.cancel()
      }
    }
  }
}
</script>
