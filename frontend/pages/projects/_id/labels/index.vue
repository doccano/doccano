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
import LabelList from '@/components/containers/LabelList'
import LabelCreationButton from '@/components/containers/LabelCreationButton'
import LabelDeletionButton from '@/components/containers/LabelDeletionButton'

export default {
  layout: 'project',

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
