<template>
  <div>
    <v-btn
      :disabled="!isDocumentSelected"
      @click="dialog=true"
      class="text-capitalize"
      outlined
    >
      Delete
    </v-btn>
    <base-dialog :dialog="dialog">
      <confirm-form
        :items="selected"
        @ok="deleteDocument($route.params.id);dialog=false"
        @cancel="dialog=false"
        title="Delete Document"
        message="Are you sure you want to delete these documents from this project?"
        item-key="text"
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
