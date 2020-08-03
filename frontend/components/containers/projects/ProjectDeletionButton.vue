<template>
  <confirm-dialog
    :disabled="!isDeletable"
    :items="selected"
    title="Delete Project"
    message="Are you sure you want to delete these projects?"
    item-key="name"
    @ok="handleDeleteProject"
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
    ...mapGetters('projects', ['isDeletable'])
  },

  methods: {
    handleDeleteProject() {
      this.$store.dispatch('projects/deleteProject')
    }
  }
}
</script>
