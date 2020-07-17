<template>
  <text-classification />
</template>

<script>
import TextClassification from '~/components/containers/annotation/TextClassification'

export default {
  layout: 'annotation',

  components: {
    TextClassification
  },

  validate({ params, query }) {
    return /^\d+$/.test(params.id) && /^\d+$/.test(query.page)
  }
}
</script>
