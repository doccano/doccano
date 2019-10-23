<template>
  <v-card>
    <v-card-title class="mb-2">
      <action-menu
        :items="menuItems"
        @upload="importDialog=true"
        @download="exportDialog=true"
      />
      <v-dialog
        v-model="importDialog"
        width="800"
      >
        <document-upload-form
          :upload-document="uploadDocument"
          :formats="formatList"
          @close="importDialog=false"
        />
      </v-dialog>
      <v-dialog
        v-model="exportDialog"
        width="800"
      >
        <document-export-form
          :export-document="exportDocument"
          :formats="['json']"
          @close="exportDialog=false"
        />
      </v-dialog>
      <v-btn
        class="text-capitalize ms-2"
        outlined
        :disabled="!isDocumentSelected"
        @click="deleteDialog=true"
      >
        Delete
      </v-btn>
      <v-dialog
        v-model="deleteDialog"
        width="800"
      >
        <confirm-form
          title="Delete Document"
          message="Are you sure you want to delete these documents from this project?"
          item-key="text"
          :items="selected"
          @ok="deleteDocument($route.params.id);deleteDialog=false"
          @cancel="deleteDialog=false"
        />
      </v-dialog>
    </v-card-title>
    <document-list />
  </v-card>
</template>

<script>
import { mapActions, mapGetters, mapState } from 'vuex'
import ActionMenu from '@/components/molecules/ActionMenu'
import ConfirmForm from '@/components/organisms/ConfirmForm'
import DocumentList from '@/components/containers/DocumentList'
import DocumentUploadForm from '@/components/organisms/DocumentUploadForm'
import DocumentExportForm from '@/components/organisms/DocumentExportForm'

export default {
  layout: 'project',

  components: {
    ActionMenu,
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
