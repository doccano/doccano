<template>
  <v-row v-if="!isEmpty">
    <v-col
      cols="12"
      lg="4"
    >
      <v-card>
        <doughnut-chart
          :chart-data="stats.progress"
        />
      </v-card>
    </v-col>
    <v-col
      cols="12"
      lg="4"
    >
      <v-card>
        <bar-chart
          :chart-data="stats.label"
        />
      </v-card>
    </v-col>
    <v-col
      cols="12"
      lg="4"
    >
      <v-card>
        <bar-chart
          :chart-data="stats.user"
        />
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import _ from 'lodash'
import DoughnutChart from '@/components/statistics/ChartDoughnut'
import BarChart from '@/components/statistics/ChartBar'

export default {
  layout: 'project',

  components: {
    DoughnutChart,
    BarChart
  },

  data() {
    return {
      stats: {}
    }
  },

  computed: {
    isEmpty() {
      return _.isEmpty(this.stats)
    }
  },

  async created() {
    this.stats = await this.$services.statistics.fetchStatistics(
      this.$route.params.id,
      this.$t('statistics.labelStats'),
      this.$t('statistics.userStats'),
      this.$t('statistics.progress')
    )
  },

  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>
