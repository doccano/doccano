<template>
  <v-card>
    <v-card-title class="mb-2">
      <action-menu
        :items="menuItems"
        @upload="importDialog=true"
        @download="exportDialog=true"
      />
      <base-dialog :dialog="importDialog">
        <document-upload-form
          :upload-document="uploadDocument"
          :formats="formatList"
          @close="importDialog=false"
        />
      </base-dialog>
      <base-dialog :dialog="exportDialog">
        <document-export-form
          :export-document="exportDocument"
          :formats="['json']"
          @close="exportDialog=false"
        />
      </base-dialog>
      <v-btn
        class="text-capitalize ms-2"
        outlined
        :disabled="!isDocumentSelected"
        @click="deleteDialog=true"
      >
        Delete
      </v-btn>
      <base-dialog :dialog="deleteDialog">
        <confirm-form
          title="Delete Document"
          message="Are you sure you want to delete these documents from this project?"
          item-key="text"
          :items="selected"
          @ok="deleteDocument($route.params.id);deleteDialog=false"
          @cancel="deleteDialog=false"
        />
      </base-dialog>
    </v-card-title>
    <document-list />
  </v-card>
</template>

<script>
import { mapActions, mapGetters, mapState } from 'vuex'
import ActionMenu from '@/components/molecules/ActionMenu'
import BaseDialog from '@/components/molecules/BaseDialog'
import ConfirmForm from '@/components/organisms/utils/ConfirmForm'
import DocumentList from '@/components/containers/documents/DocumentList'
import DocumentUploadForm from '@/components/organisms/documents/DocumentUploadForm'
import DocumentExportForm from '@/components/organisms/documents/DocumentExportForm'

export default {
  layout: 'project',

  middleware: 'check-auth',

  components: {
    ActionMenu,
    BaseDialog,
    ConfirmForm,
    DocumentList,
    DocumentUploadForm,
    DocumentExportForm
  },

  data() {
    return {
      importDialog: false,
      exportDialog: false,
      deleteDialog: false,
      menuItems: [
        { title: 'Import', icon: 'backup', event: 'upload' },
        { title: 'Export', icon: 'archive', event: 'download' }
      ]
    }
  },

  computed: {
    ...mapGetters('documents', ['formatList', 'isDocumentSelected']),
    ...mapState('documents', ['selected'])
  },

  methods: {
    ...mapActions('documents', ['uploadDocument', 'exportDocument', 'deleteDocument'])
  },

  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>
