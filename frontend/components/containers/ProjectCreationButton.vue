<template>
  <v-dialog
    v-model="dialog"
    width="800px"
  >
    <template v-slot:activator="{ on }">
      <v-btn
        class="mb-2 text-capitalize"
        color="primary"
        @click="dialog=true"
      >
        Add Project
      </v-btn>
    </template>
    <project-creation-form
      :create-project="createProject"
      @close="dialog=false"
    />
  </v-dialog>
</template>

<script>
import { mapActions } from 'vuex'
import ProjectCreationForm from '@/components/organisms/ProjectCreationForm'

export default {
  components: {
    ProjectCreationForm
  },

  data() {
    return {
      dialog: false
    }
  },

  methods: {
    ...mapActions('projects', ['createProject'])
  }
}
</script>
