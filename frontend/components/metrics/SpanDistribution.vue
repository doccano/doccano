<template>
  <label-distribution
    title="Span Distribution"
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
    this.distribution = await this.$services.metrics.fetchSpanDistribution(this.$route.params.id)
    this.labels = await this.$services.spanType.list(this.$route.params.id)
  }
})
</script>
