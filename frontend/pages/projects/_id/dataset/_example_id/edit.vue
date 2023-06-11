<template>
  <v-card>
    <v-card-title>Edit Text</v-card-title>
    <v-card-text>
      <v-form ref="form" v-model="valid">
        <v-textarea
          v-model="editedItem.text"
          autofocus
          auto-grow
          counter
          outlined
          :rules="[rules.required]"
        />
        <v-btn :disabled="!valid" color="primary" class="text-capitalize" @click="save">
          Save
        </v-btn>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import { Project } from '~/domain/models/project/project'
import { ExampleDTO } from '~/services/application/example/exampleData'

export default Vue.extend({
  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject', 'isProjectAdmin'],

  validate({ params, store }) {
    if (/^\d+$/.test(params.id) && /^\d+$/.test(params.example_id)) {
      const project = store.getters['projects/project'] as Project
      return project.isTextProject
    }
    return false
  },

  data() {
    return {
      editedItem: {} as ExampleDTO,
      valid: true,
      rules: {
        required: (v: string) => !!v || 'Required'
      }
    }
  },

  computed: {
    projectId(): string {
      return this.$route.params.id
    }
  },

  async created() {
    const exampleId = parseInt(this.$route.params.example_id, 10)
    this.editedItem = await this.$services.example.findById(this.projectId, exampleId)
  },

  methods: {
    async save() {
      await this.$services.example.update(this.projectId, this.editedItem)
      this.$router.push(`/projects/${this.projectId}/dataset`)
    }
  }
})
</script>
