<template>
  <base-modal
    text="Upload"
    :is-create="true"
  >
    <template v-slot="slotProps">
      <document-upload-form
        :upload-document="uploadDocument"
        :formats="formatList"
        @close="slotProps.close"
      />
    </template>
  </base-modal>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import BaseModal from '@/components/molecules/BaseModal'
import DocumentUploadForm from '@/components/organisms/DocumentUploadForm'

export default {
  components: {
    BaseModal,
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
