<template>
  <v-card>
    <v-card-title class="mb-2">
      <document-action-menu />
      <document-deletion-button class="ms-2" />
    </v-card-title>
    <document-list />
  </v-card>
</template>

<script>
import DocumentList from '@/components/containers/documents/DocumentList'
import DocumentActionMenu from '@/components/containers/documents/DocumentActionMenu'
import DocumentDeletionButton from '@/components/containers/documents/DocumentDeletionButton'

export default {
  layout: 'project',

  middleware: ['check-auth', 'auth', 'check-admin'],

  components: {
    DocumentList,
    DocumentActionMenu,
    DocumentDeletionButton
  },

  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>
