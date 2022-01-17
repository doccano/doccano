<template>
  <label-distribution
    title="Span Distribution"
    :distribution="distribution"
    :color-mapping="colorMapping"
  />
</template>

<script lang="ts">
import Vue from 'vue'
import LabelDistribution from './LabelDistribution.vue'

export default Vue.extend({
  components: {
    LabelDistribution
  },

  data() {
    return {
      distribution: {},
      colorMapping: {},
    }
  },

  async created() {
    this.distribution = await this.$services.metrics.fetchSpanDistribution(this.$route.params.id)
    const labels = await this.$services.spanType.list(this.$route.params.id)
    this.colorMapping = Object.fromEntries(labels.map((label) => [label.text, label.backgroundColor]))
  }
})
</script>
