<template>
  <div>
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
        :formats="getImportFormat"
        @close="importDialog=false"
      />
    </v-dialog>
    <v-dialog
      v-model="exportDialog"
      width="800"
    >
      <document-export-form
        :export-document="exportDocument"
        :formats="getExportFormat"
        @close="exportDialog=false"
      />
    </v-dialog>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import ActionMenu from '@/components/molecules/ActionMenu'
import DocumentUploadForm from '@/components/organisms/documents/DocumentUploadForm'
import DocumentExportForm from '@/components/organisms/documents/DocumentExportForm'

export default {
  components: {
    ActionMenu,
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
