<template>
  <v-card>
    <v-card-title>
      <document-deletion-button />
    </v-card-title>
    <document-list />
  </v-card>
</template>

<script>
import DocumentList from '@/components/containers/DocumentList'
// import DocumentCreationButton from '@/components/containers/DocumentCreationButton'
import DocumentDeletionButton from '@/components/containers/DocumentDeletionButton'

export default {
  layout: 'project',
  components: {
    DocumentList,
    // DocumentCreationButton,
    DocumentDeletionButton
  },
  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>
