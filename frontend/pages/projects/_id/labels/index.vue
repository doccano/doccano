<template>
  <v-card>
    <label-list />
  </v-card>
</template>

<script>
import LabelList from '@/components/label/LabelList'

export default {
  layout: 'project',

  components: {
    LabelList
  },

  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>
