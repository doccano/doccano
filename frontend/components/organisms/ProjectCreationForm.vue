<template>
  <base-card title="Add Project">
    <template #content>
      <v-form
        ref="form"
        v-model="valid"
      >
        <v-text-field
          v-model="name"
          :rules="nameRules"
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
          :rules="[v => !!v || 'Type is required']"
          label="projectType"
          prepend-icon="mdi-keyboard"
          data-test="project-type"
          required
        />
      </v-form>
    </template>
    <template #actions>
      <v-btn
        class="text-capitalize"
        text
        color="primary"
        data-test="cancel-button"
        @click="cancel"
      >
        Cancel
      </v-btn>
      <v-btn
        :disabled="!valid"
        class="text-none"
        text
        data-test="create-button"
        @click="create"
      >
        Create
      </v-btn>
    </template>
  </base-card>
</template>

<script>
import BaseCard from '@/components/molecules/BaseCard'

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
      valid: true,
      name: '',
      description: '',
      projectType: null,
      nameRules: [
        v => !!v || 'Project name is required',
        v =>
          (v && v.length <= 30) || 'Project name must be less than 30 characters'
      ],
      descriptionRules: [
        v => !!v || 'Description is required',
        v =>
          (v && v.length <= 100) || 'Description must be less than 100 characters'
      ]
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
        this.createProject({
          name: this.name,
          description: this.description,
          project_type: this.projectType
        })
        this.reset()
        this.cancel()
      }
    }
  }
}
</script>
