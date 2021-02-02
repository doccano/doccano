<template>
  <v-card>
    <v-card-title>
      <comment-deletion-button />
    </v-card-title>
    <comment-list />
  </v-card>
</template>

<script>
import CommentList from '@/components/containers/comments/CommentList'
import CommentDeletionButton from '@/components/containers/comments/CommentDeletionButton'

export default {
  layout: 'project',

  components: {
    CommentList,
    CommentDeletionButton
  },

  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>
