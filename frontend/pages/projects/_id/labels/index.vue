<template>
  <v-card>
    <v-card-title class="mb-2">
      <label-action-menu />
      <label-deletion-button class="ms-2" />
    </v-card-title>
    <label-list />
  </v-card>
</template>

<script>
import LabelList from '@/components/containers/labels/LabelList'
import LabelActionMenu from '@/components/containers/labels/LabelActionMenu'
import LabelDeletionButton from '@/components/containers/labels/LabelDeletionButton'

export default {
  layout: 'project',

  components: {
    LabelList,
    LabelActionMenu,
    LabelDeletionButton
  },

  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>
