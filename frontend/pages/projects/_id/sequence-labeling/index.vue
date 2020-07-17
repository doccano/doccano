<template>
  <v-card>
    <v-card-text class="title">
      <entity-item-box />
    </v-card-text>
  </v-card>
</template>

<script>
import EntityItemBox from '~/components/containers/annotation/EntityItemBox'

export default {
  layout: 'annotation',

  components: {
    EntityItemBox
  },

  validate({ params, query }) {
    return /^\d+$/.test(params.id) && /^\d+$/.test(query.page)
  }
}
</script>
