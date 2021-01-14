<template>
  <div>
    <action-menu
      :items="menuItems"
      @upload="importDialog=true"
      @download="exportDialog=true"
    />
    <base-dialog :dialog="importDialog">
      <document-upload-form
        :upload-document="uploadDocument"
        :formats="getImportFormat"
        @close="importDialog=false"
      />
    </base-dialog>
    <base-dialog :dialog="exportDialog">
      <document-export-form
        :export-document="exportDocument"
        :formats="getExportFormat"
        @close="exportDialog=false"
      />
    </base-dialog>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import ActionMenu from '@/components/molecules/ActionMenu'
import BaseDialog from '@/components/molecules/BaseDialog'
import DocumentUploadForm from '@/components/organisms/documents/DocumentUploadForm'
import DocumentExportForm from '@/components/organisms/documents/DocumentExportForm'

export default {
  components: {
    ActionMenu,
    BaseDialog,
    DocumentUploadForm,
    DocumentExportForm
  },

  data() {
    return {
      importDialog: false,
      exportDialog: false,
      menuItems: [
        { title: 'Import Dataset', icon: 'mdi-upload', event: 'upload' },
        { title: 'Export Dataset', icon: 'mdi-download', event: 'download' }
      ]
    }
  },

  computed: {
    ...mapGetters('projects', ['getImportFormat', 'getExportFormat'])
  },

  created() {
    this.setCurrentProject(this.$route.params.id)
  },

  methods: {
    ...mapActions('documents', ['uploadDocument', 'exportDocument']),
    ...mapActions('projects', ['setCurrentProject'])
  }
}
</script>
