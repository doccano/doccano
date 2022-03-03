<template>
  <v-row>
    <v-col cols="12">
      <member-progress />
    </v-col>
    <v-col v-if="!!project.hasCategory" cols="12">
      <label-distribution
        title="Category Distribution"
        :distribution="categoryDistribution"
        :label-types="categoryTypes"
      />
    </v-col>
    <v-col v-if="!!project.hasSpan" cols="12">
      <label-distribution
        title="Span Distribution"
        :distribution="spanDistribution"
        :label-types="spanTypes"
      />
    </v-col>
    <v-col v-if="!!project.useRelation" cols="12">
      <label-distribution
        title="Relation Distribution"
        :distribution="relationDistribution"
        :label-types="relationTypes"
      />
    </v-col>
  </v-row>
</template>

<script>
import LabelDistribution from '~/components/metrics/LabelDistribution'
import MemberProgress from '~/components/metrics/MemberProgress'

export default {
  components: {
    LabelDistribution,
    MemberProgress,
  },
  
  layout: 'project',

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  data() {
    return {
      project: {},
      categoryTypes: [],
      categoryDistribution: {},
      relationTypes: [],
      relationDistribution: {},
      spanTypes: [],
      spanDistribution: {},
    }
  },

  computed: {
    projectId() {
      return this.$route.params.id
    }
  },

  async created() {
    this.project = await this.$services.project.findById(this.projectId)
    if (this.project.hasCategory) {
      this.categoryTypes = await this.$services.categoryType.list(this.projectId)
      this.categoryDistribution = await this.$services.metrics.fetchCategoryDistribution(this.projectId)
    }
    if (this.project.hasSpan) {
      this.spanTypes = await this.$services.spanType.list(this.projectId)
      this.spanDistribution = await this.$services.metrics.fetchSpanDistribution(this.projectId)
    }
    if (this.project.useRelation) {
      this.relationTypes = await this.$services.relationType.list(this.projectId)
      this.relationDistribution = await this.$services.metrics.fetchRelationDistribution(this.projectId)
    }
  }
}
</script>
