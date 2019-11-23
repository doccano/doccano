<template>
  <confirm-dialog
    title="Remove Member"
    message="Are you sure you want to remove these members?"
    item-key="username"
    :disabled="!isMemberSelected"
    :items="selected"
    @ok="handleRemoveMember()"
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
    ...mapState('members', ['selected']),
    ...mapGetters('members', ['isMemberSelected'])
  },

  methods: {
    ...mapActions('members', ['removeMember']),

    handleRemoveMember() {
      const projectId = this.$route.params.id
      this.removeMember(projectId)
    }
  }
}
</script>
