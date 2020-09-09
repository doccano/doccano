<template>
  <div>
    <v-btn
      :disabled="!hasDocuments"
      class="text-capitalize"
      outlined
      @click="dialog=true"
    >
      Delete all
    </v-btn>
    <v-dialog
      v-model="dialog"
      width="800"
    >
      <confirm-form
        :items="selected"
        title="Delete All Documents"
        message="Are you sure you want to delete all documents from this project?"
        item-key="text"
        @ok="deleteAllDocuments($route.params.id);dialog=false"
        @cancel="dialog=false"
      />
    </v-dialog>
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'
import ConfirmForm from '@/components/organisms/utils/ConfirmForm'

export default {
  components: {
    ConfirmForm
  },

  data() {
    return {
      dialog: false
    }
  },

  computed: {
    ...mapState('documents', ['selected']),
    ...mapGetters('documents', ['hasDocuments'])
  },

  methods: {
    ...mapActions('documents', ['deleteAllDocuments']),

    handleDeleteAllDocuments() {
      const projectId = this.$route.params.id
      this.deleteAllDocuments(projectId)
    }
  }
}
</script>
