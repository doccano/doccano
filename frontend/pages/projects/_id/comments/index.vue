<template>
  <v-card>
    <comment-list />
  </v-card>
</template>

<script>
import CommentList from '@/components/containers/comments/CommentList'

export default {
  layout: 'project',

  components: {
    CommentList
  },

  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>
