<template>
  <base-modal
    text="Upload"
    :is-create="true"
  >
    <template v-slot="slotProps">
      <document-upload-form
        :upload-document="uploadDocument"
        @close="slotProps.close"
      />
    </template>
  </base-modal>
</template>

<script>
import { mapActions } from 'vuex'
import BaseModal from '@/components/molecules/BaseModal'
import DocumentUploadForm from '@/components/organisms/DocumentUploadForm'

export default {
  components: {
    BaseModal,
    DocumentUploadForm
  },

  methods: {
    ...mapActions('documents', ['uploadDocument'])
  }
}
</script>
