<template>
  <v-card>
    <v-card-title class="mb-2">
      <document-action-menu />
      <document-deletion-button class="ms-2" />
      <document-bulk-deletion-button class="ms-2" />
    </v-card-title>
    <document-list />
  </v-card>
</template>

<script>
import DocumentList from '@/components/containers/documents/DocumentList'
import DocumentActionMenu from '@/components/containers/documents/DocumentActionMenu'
import DocumentDeletionButton from '@/components/containers/documents/DocumentDeletionButton'
import DocumentBulkDeletionButton from '@/components/containers/documents/DocumentBulkDeletionButton'

export default {
  layout: 'project',

  components: {
    DocumentList,
    DocumentActionMenu,
    DocumentDeletionButton,
    DocumentBulkDeletionButton
  },

  validate({ params, query }) {
    return /^\d+$/.test(params.id) && /^\d+|$/.test(query.limit) && /^\d+|$/.test(query.offset)
  }
}
</script>
