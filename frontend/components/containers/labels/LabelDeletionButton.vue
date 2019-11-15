<template>
  <confirm-dialog
    title="Delete Label"
    message="Are you sure you want to remove these labels from this project?"
    item-key="text"
    :disabled="!isLabelSelected"
    :items="selected"
    @ok="handleDeleteLabel()"
  />
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'
import ConfirmDialog from '@/components/organisms/utils/ConfirmDialog'

export default {
  components: {
    ConfirmDialog
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
