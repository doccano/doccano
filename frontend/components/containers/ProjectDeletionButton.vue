<template>
  <base-modal
    text="Delete"
    :disabled="!isProjectSelected"
  >
    <template v-slot="slotProps">
      <project-deletion-form
        :selected="selected"
        @delete="handleDeleteProject(); slotProps.close()"
        @close="slotProps.close"
      />
    </template>
  </base-modal>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import BaseModal from '@/components/molecules/BaseModal'
import ProjectDeletionForm from '@/components/organisms/ProjectDeletionForm'

export default {
  components: {
    BaseModal,
    ProjectDeletionForm
  },

  computed: {
    ...mapState('projects', ['selected']),
    ...mapGetters('projects', ['isProjectSelected'])
  },

  methods: {
    handleDeleteProject() {
      this.$store.dispatch('projects/deleteProject')
    }
  }
}
</script>
