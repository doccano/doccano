<template>
  <v-card>
    <v-card-title>
      <document-upload-button />
      <document-deletion-button />
    </v-card-title>
    <document-list />
  </v-card>
</template>

<script>
import DocumentList from '@/components/containers/DocumentList'
import DocumentUploadButton from '@/components/containers/DocumentUploadButton'
import DocumentDeletionButton from '@/components/containers/DocumentDeletionButton'

export default {
  layout: 'project',
  components: {
    DocumentList,
    DocumentUploadButton,
    DocumentDeletionButton
  },
  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>
