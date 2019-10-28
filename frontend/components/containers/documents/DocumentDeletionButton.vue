<template>
  <confirm-dialog
    title="Delete Document"
    message="Are you sure you want to delete these documents from this project?"
    item-key="text"
    :disabled="!isDocumentSelected"
    :items="selected"
    @ok="handleDeleteDocument()"
  />
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'
import ConfirmDialog from '@/components/organisms/utils/ConfirmDialog'

export default {
  components: {
    ConfirmDialog
  },

  computed: {
    ...mapState('documents', ['selected']),
    ...mapGetters('documents', ['isDocumentSelected'])
  },

  methods: {
    ...mapActions('documents', ['deleteDocument']),

    handleDeleteDocument() {
      const projectId = this.$route.params.id
      this.deleteDocument(projectId)
    }
  }
}
</script>
