<template>
  <label-distribution
    title="Category Distribution"
    :distribution="distribution"
    :labels="labels"
  />
</template>

<script lang="ts">
import Vue from 'vue'
import LabelDistribution from './LabelDistribution.vue'
import { LabelDTO } from '~/services/application/label/labelData'

export default Vue.extend({
  components: {
    LabelDistribution
  },

  data() {
    return {
      distribution: {},
      labels: [] as LabelDTO[],
    }
  },

  async created() {
    this.distribution = await this.$services.metrics.fetchCategoryDistribution(this.$route.params.id)
    this.labels = await this.$services.categoryType.list(this.$route.params.id)
  }
})
</script>
