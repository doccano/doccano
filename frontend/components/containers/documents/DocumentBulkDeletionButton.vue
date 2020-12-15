<template>
  <div>
    <v-btn
      :disabled="!total"
      class="text-capitalize"
      outlined
      @click="dialog=true"
    >
      {{ $t('generic.deleteAll') }}
    </v-btn>
    <v-dialog
      v-model="dialog"
      width="800"
    >
      <confirm-form
        :title="$t('dataset.deleteBulkDocumentsTitle')"
        :message="$t('dataset.deleteBulkDocumentsMessage')"
        :button-true-text="$t('generic.yes')"
        :button-false-text="$t('generic.cancel')"
        item-key="text"
        @ok="deleteAllDocuments($route.params.id);dialog=false"
        @cancel="dialog=false"
      />
    </v-dialog>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
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
    ...mapState('documents', ['total'])
  },

  methods: {
    ...mapActions('documents', ['deleteAllDocuments'])
  }
}
</script>
