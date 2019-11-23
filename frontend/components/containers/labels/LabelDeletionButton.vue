<template>
  <div>
    <v-btn
      class="text-capitalize"
      outlined
      :disabled="!isLabelSelected"
      @click="dialog=true"
    >
      Delete
    </v-btn>
    <base-dialog :dialog="dialog">
      <confirm-form
        title="Delete Label"
        message="Are you sure you want to delete these labels from this project?"
        item-key="text"
        :items="selected"
        @ok="deleteLabel($route.params.id);dialog=false"
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
    ...mapState('labels', ['selected']),
    ...mapGetters('labels', ['isLabelSelected'])
  },

  methods: {
    ...mapActions('labels', ['deleteLabel']),

    handleDeleteLabel() {
      const projectId = this.$route.params.id
      this.deleteLabel(projectId)
    }
  }
}
</script>
