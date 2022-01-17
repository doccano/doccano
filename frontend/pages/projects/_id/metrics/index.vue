<template>
  <v-row>
    <v-col cols="12">
      <member-progress />
    </v-col>
    <v-col v-if="!!project.hasCategory" cols="12">
      <category-distribution />
    </v-col>
    <v-col v-if="!!project.hasSpan" cols="12">
      <span-distribution />
    </v-col>
  </v-row>
</template>

<script>
import CategoryDistribution from '~/components/metrics/CategoryDistribution'
import SpanDistribution from '~/components/metrics/SpanDistribution'
import MemberProgress from '~/components/metrics/MemberProgress'

export default {
  components: {
    CategoryDistribution,
    SpanDistribution,
    MemberProgress
  },
  
  layout: 'project',

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  data() {
    return {
      project: {},
    }
  },

  async created() {
    this.project = await this.$services.project.findById(this.$route.params.id)
  }
}
</script>
