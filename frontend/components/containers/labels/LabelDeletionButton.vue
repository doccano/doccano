<template>
  <div>
    <v-btn
      :disabled="!isLabelSelected"
      class="text-capitalize"
      outlined
      @click="dialog=true"
    >
      Delete
    </v-btn>
    <v-dialog
      v-model="dialog"
      width="800"
    >
      <confirm-form
        :items="selected"
        title="Delete Label"
        message="Are you sure you want to delete these labels from this project?"
        item-key="text"
        @ok="deleteLabel($route.params.id);dialog=false"
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
