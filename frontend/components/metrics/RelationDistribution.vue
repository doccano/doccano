<template>
  <label-distribution
    title="Relation Distribution"
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
    this.distribution = await this.$services.metrics.fetchRelationDistribution(this.$route.params.id)
    const labels = await this.$services.relationType.list(this.$route.params.id)
    this.colorMapping = Object.fromEntries(labels.map((label) => [label.text, label.backgroundColor]))
  }
})
</script>
