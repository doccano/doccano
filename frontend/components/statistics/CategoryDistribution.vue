<template>
  <label-distribution
    title="Category Distribution"
    :distribution="distribution"
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
      distribution: {}
    }
  },

  async created() {
    this.distribution = await this.$services.statistics.fetchCategoryDistribution(this.$route.params.id)
  }
})
</script>