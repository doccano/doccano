<template>
  <seq2seq-container />
</template>

<script>
import Seq2seqContainer from '~/components/containers/annotation/Seq2seqContainer'

export default {
  layout: 'annotation',

  components: {
    Seq2seqContainer
  },

  validate({ params, query }) {
    return /^\d+$/.test(params.id) && /^\d+$/.test(query.page)
  }
}
</script>
