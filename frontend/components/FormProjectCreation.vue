<template>
  <v-card>
    <v-card-title class="grey lighten-2">
      Create Project
    </v-card-title>
    <v-container grid-list-sm>
      <v-layout wrap>
        <v-flex xs12>
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
        </v-flex>
      </v-layout>
    </v-container>
    <v-card-actions>
      <v-spacer />
      <v-btn
        class="text-capitalize"
        text
        color="primary"
        @click="cancel"
      >
        Cancel
      </v-btn>
      <v-btn
        :disabled="!valid"
        class="text-none"
        text
        @click="createProject"
      >
        Add Project
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import ProjectService from '~/services/project.service'

export default {
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

    async createProject() {
      const data = {
        name: this.name,
        description: this.description,
        project_type: this.projectType
      }
      if (this.$refs.form.validate()) {
        const response = await ProjectService.createProject(data)
        this.$refs.form.reset()
        this.$emit('create-project', response)
      }
    }
  }
}
</script>
