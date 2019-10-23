<template>
  <v-card>
    <v-card-title class="mb-2">
      <v-menu offset-y>
        <template v-slot:activator="{ on }">
          <v-btn
            color="text-capitalize primary"
            v-on="on"
          >
            Actions
            <v-icon>mdi-menu-down</v-icon>
          </v-btn>
        </template>
        <v-list dense>
          <v-list-item @click="uploadDialog=true">
            <v-list-item-icon>
              <v-icon>backup</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Upload</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-dialog
        v-model="uploadDialog"
        width="800"
      >
        <document-upload-form
          :upload-document="uploadDocument"
          :formats="formatList"
          @close="uploadDialog=false"
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
import ConfirmForm from '@/components/organisms/ConfirmForm'
import DocumentList from '@/components/containers/DocumentList'
import DocumentUploadForm from '@/components/organisms/DocumentUploadForm'

export default {
  layout: 'project',

  components: {
    ConfirmForm,
    DocumentList,
    DocumentUploadForm
  },

  data() {
    return {
      uploadDialog: false,
      deleteDialog: false
    }
  },

  computed: {
    ...mapGetters('documents', ['formatList', 'isDocumentSelected']),
    ...mapState('documents', ['selected'])
  },

  methods: {
    ...mapActions('documents', ['uploadDocument', 'deleteDocument'])
  },

  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>
