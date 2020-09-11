<template>
  <div>
    <v-btn
      :disabled="!isDocumentSelected"
      class="text-capitalize"
      outlined
      @click="dialog=true"
    >
      {{ $t('generic.delete') }}
    </v-btn>
    <v-dialog
      v-model="dialog"
      width="800"
    >
      <confirm-form
        :items="selected"
        :title="$t('dataset.deleteDocumentsTitle')"
        :message="$t('dataset.deleteDocumentsMessage')"
        :button-true-text="$t('generic.yes')"
        :button-false-text="$t('generic.cancel')"
        item-key="text"
        @ok="deleteDocument($route.params.id);dialog=false"
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
