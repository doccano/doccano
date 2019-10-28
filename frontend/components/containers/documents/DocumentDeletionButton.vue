<template>
  <div>
    <v-btn
      class="text-capitalize"
      outlined
      :disabled="!isDocumentSelected"
      @click="dialog=true"
    >
      Delete
    </v-btn>
    <base-dialog :dialog="dialog">
      <confirm-form
        title="Delete Document"
        message="Are you sure you want to delete these documents from this project?"
        item-key="text"
        :items="selected"
        @ok="deleteDocument($route.params.id);dialog=false"
        @cancel="dialog=false"
      />
    </base-dialog>
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'
import BaseDialog from '@/components/molecules/BaseDialog'
import ConfirmForm from '@/components/organisms/utils/ConfirmForm'

export default {
  components: {
    BaseDialog,
    ConfirmForm
  },

  data() {
    return {
      dialog: false
    }
  },

  computed: {
    ...mapState('documents', ['selected']),
    ...mapGetters('documents', ['isDocumentSelected'])
  },

  methods: {
    ...mapActions('documents', ['deleteDocument']),

    handleDeleteDocument() {
      const projectId = this.$route.params.id
      this.deleteDocument(projectId)
    }
  }
}
</script>
