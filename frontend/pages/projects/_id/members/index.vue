<template>
  <v-card>
    <v-card-title>
      <member-addition-button />
      <member-deletion-button />
    </v-card-title>
    <member-list />
  </v-card>
</template>

<script>
import MemberList from '@/components/containers/members/MemberList'
import MemberAdditionButton from '@/components/containers/members/MemberAdditionButton'
import MemberDeletionButton from '@/components/containers/members/MemberDeletionButton'

export default {
  layout: 'project',

  middleware: ['check-auth', 'auth', 'check-admin'],

  components: {
    MemberList,
    MemberAdditionButton,
    MemberDeletionButton
  },

  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>
