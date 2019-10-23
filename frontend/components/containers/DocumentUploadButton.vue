<template>
  <document-upload-form
    :upload-document="uploadDocument"
    :formats="formatList"
    @close="slotProps.close"
  />
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import DocumentUploadForm from '@/components/organisms/DocumentUploadForm'

export default {
  components: {
    DocumentUploadForm
  },

  computed: {
    ...mapGetters('documents', ['formatList'])
  },

  methods: {
    ...mapActions('documents', ['uploadDocument'])
  }
}
</script>
