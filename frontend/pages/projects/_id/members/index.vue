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
import MemberList from '@/components/containers/MemberList'
import MemberAdditionButton from '@/components/containers/MemberAdditionButton'
import MemberDeletionButton from '@/components/containers/MemberDeletionButton'

export default {
  layout: 'project',

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
