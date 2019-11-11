<template>
  <v-card>
    <v-card-title>
      <label-creation-button />
      <label-deletion-button />
    </v-card-title>
    <label-list />
  </v-card>
</template>

<script>
import LabelList from '@/components/containers/labels/LabelList'
import LabelCreationButton from '@/components/containers/labels/LabelCreationButton'
import LabelDeletionButton from '@/components/containers/labels/LabelDeletionButton'

export default {
  layout: 'project',

  middleware: ['check-auth', 'auth', 'check-admin'],

  components: {
    LabelList,
    LabelCreationButton,
    LabelDeletionButton
  },

  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>
