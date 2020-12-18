<template>
  <v-tooltip bottom>
    <template v-slot:activator="{ on }">
      <v-btn
        class="text-capitalize ps-1 pe-1"
        color="error"
        min-width="36"
        icon
        v-on="on"
        @click="dialog=true"
      >
        <v-icon>
          mdi-delete-outline
        </v-icon>
      </v-btn>
    </template>
    <span>Clear Annotations</span>
    <v-dialog
      v-model="dialog"
      width="800"
    >
      <confirm-form
        title="Clear annotations"
        message="Are you sure you want to delete all annotations?"
        :button-true-text="$t('generic.yes')"
        :button-false-text="$t('generic.cancel')"
        @ok="handleClear();dialog=false"
        @cancel="dialog=false"
      />
    </v-dialog>
  </v-tooltip>
</template>

<script>
import { mapActions } from 'vuex'
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

  methods: {
    ...mapActions('documents', ['clearAnnotations']),

    handleClear() {
      const projectId = this.$route.params.id
      this.clearAnnotations(projectId)
    }
  }
}
</script>
