<template>
  <v-dialog
    v-model="dialog"
    width="800px"
  >
    <template v-slot:activator="{ on }">
      <v-btn
        class="mb-2 ml-2 text-capitalize"
        outlined
        :disabled="!isProjectSelected"
        @click="dialog=true"
      >
        Delete
      </v-btn>
    </template>
    <project-deletion-form
      :selected="selected"
      @delete="handleDeleteProject"
      @close="dialog=false"
    />
  </v-dialog>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import ProjectDeletionForm from '@/components/organisms/ProjectDeletionForm'

export default {
  components: {
    ProjectDeletionForm
  },

  data() {
    return {
      dialog: false
    }
  },

  computed: {
    ...mapState('projects', ['selected']),
    ...mapGetters('projects', ['isProjectSelected'])
  },

  methods: {
    handleDeleteProject() {
      this.$store.dispatch('projects/deleteProject')
      this.dialog = false
    }
  }
}
</script>
