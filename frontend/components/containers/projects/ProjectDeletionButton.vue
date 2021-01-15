<template>
  <confirm-dialog
    :disabled="!isProjectSelected"
    :items="selected"
    @ok="handleDeleteProject"
    title="Delete Project"
    message="Are you sure you want to delete these projects?"
    item-key="name"
  />
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import ConfirmDialog from '@/components/organisms/utils/ConfirmDialog'

export default {
  components: {
    ConfirmDialog
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
