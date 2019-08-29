<template>
  <base-card
    title="Create Project"
    button="Add Project"
    :disabled="!valid"
    @cancel="cancel"
    @agree="createProject"
  >
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
          required
          autofocus
        />
        <v-text-field
          v-model="description"
          :rules="descriptionRules"
          label="Description"
          prepend-icon="mdi-clipboard-text"
          required
        />
        <v-select
          v-model="projectType"
          :items="projectTypes"
          :rules="[v => !!v || 'Type is required']"
          label="projectType"
          prepend-icon="mdi-keyboard"
          required
        />
      </v-form>
    </template>
  </base-card>
</template>

<script>
import BaseCard from '~/components/BaseCard'

export default {
  components: {
    BaseCard
  },
  data: () => ({
    valid: true,
    name: '',
    description: '',
    projectType: null,
    projectTypes: [
      'Text Classification',
      'Sequence Labeling',
      'Sequence to sequence'
    ], // Todo: Get project types from backend server.
    nameRules: [
      v => !!v || 'Project name is required',
      v => (v && v.length <= 30) || 'Project name must be less than 30 characters'
    ],
    descriptionRules: [
      v => !!v || 'Description is required',
      v => (v && v.length <= 100) || 'Description must be less than 100 characters'
    ]
  }),

  methods: {
    cancel() {
      this.$emit('cancel')
    },

    createProject() {
      const data = {
        name: this.name,
        description: this.description,
        project_type: this.projectType
      }
      if (this.$refs.form.validate()) {
        this.$refs.form.reset()
        this.$emit('create-project', data)
      }
    }
  }
}
</script>
