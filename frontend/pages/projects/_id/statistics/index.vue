<template>
  <v-row>
    <v-col cols="12">
      <member-progress />
    </v-col>
    <v-col cols="12">
      <category-distribution />
    </v-col>
    <v-col cols="12">
      <span-distribution />
    </v-col>
  </v-row>
</template>

<script>
import CategoryDistribution from '~/components/statistics/CategoryDistribution'
import SpanDistribution from '~/components/statistics/SpanDistribution'
import MemberProgress from '~/components/statistics/MemberProgress'

export default {
  components: {
    CategoryDistribution,
    SpanDistribution,
    MemberProgress
  },
  
  layout: 'project',

  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>
