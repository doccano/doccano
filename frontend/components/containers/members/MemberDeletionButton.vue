<template>
  <confirm-dialog
    :disabled="!isMemberSelected"
    :items="selected"
    :title="$t('members.removeMember')"
    :message="$t('members.removePrompt')"
    :button-true-text="$t('generic.yes')"
    :button-false-text="$t('generic.cancel')"
    item-key="username"
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
