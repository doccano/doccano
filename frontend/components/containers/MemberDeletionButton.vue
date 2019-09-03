<template>
  <base-modal
    text="Remove"
    :disabled="!isMemberSelected"
  >
    <template v-slot="slotProps">
      <member-deletion-form
        :selected="selected"
        @remove="handleRemoveMember(); slotProps.close()"
        @close="slotProps.close"
      />
    </template>
  </base-modal>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'
import BaseModal from '@/components/molecules/BaseModal'
import MemberDeletionForm from '@/components/organisms/MemberDeletionForm'

export default {
  components: {
    BaseModal,
    MemberDeletionForm
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
